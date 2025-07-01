from email.headerregistry import Address
from http.client import HTTPResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from account.models import UserAddress
from . cart_module import Cart
from product.models import Product
from . import models
from .models import OrderItem, Coupon, Order
from django.conf import settings
import requests
import json

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/cart/verify'


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/cart_detail.html',{'cart':cart})


class AddToCartView(View):

    def post(self, request, pk):

        product = get_object_or_404(Product, id=pk)
        quantity, color, size = request.POST.get('quantity'), request.POST.get('color', 'empty'), request.POST.get('size', 'empty')
        cart = Cart(request)
        cart.add(product, quantity, color, size)
        return redirect('product:product-detail', pk=product.id)


class DeleteFromCartView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('cart:cart-detail')

class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        order = get_object_or_404(models.Order, id=id)
        return render(request, 'cart/order_detail.html', {'order':order})

class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = models.Order.objects.create(user=request.user, total_price=cart.total())
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'],
                                     price=item['price'], size=item['size'], color=item['color'], total_price=item['total'])
        cart.delete_cart(request)
        return redirect('cart:order-detail', order.pk)

class ApplyCouponView(LoginRequiredMixin, View):
    def post(self, request, id):
        order = get_object_or_404(models.Order, id=id)
        coupon_code = request.POST.get('coupon')
        coupon = get_object_or_404(Coupon, code=coupon_code)
        if coupon.quantity == 0:
            return redirect('cart:order-detail', order.pk)
        order.total_price -= order.total_price * coupon.discount/100
        order.save()
        return redirect('cart:order-detail', order.pk)


class SendRequest(LoginRequiredMixin, View):
    def post(self, request, id):
        order = get_object_or_404(models.Order, id=id)
        address = get_object_or_404(UserAddress, id=request.POST.get('address'))
        order.address = f'{address.address} --- {address.phone}'
        order.save()
        request.session['order_id'] = order.id
        print(order.address)
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": order.total_price,
            "description": description,
            "phone": request.user.phone,
            "callback_url": CallbackURL,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if 'data' in response and response['data'].get('code') == 100:
                    authority = response['data']['authority']
                    return HttpResponseRedirect(ZP_API_STARTPAY + authority)
                else:
                    error_message = response.get('errors', {}).get('message', 'خطای نامشخص')
                    return HttpResponse(f"خطا در پرداخت: {error_message}")

            print("Status Code:", response.status_code)
            print("Response Text:", response.text)
            return HttpResponse("خطا در ارتباط با درگاه پرداخت")


        except requests.exceptions.Timeout:
            return JsonResponse({'status': False, 'code': 'timeout'})
        except requests.exceptions.ConnectionError:
            return HttpResponse("خطای اتصال به درگاه پرداخت")

class Verify(LoginRequiredMixin, View):
    def get(self, request):
        authority = request.GET.get('Authority')
        order_id = request.session['order_id']
        order = Order.objects.get(id=order_id)
        print(authority, order.id)
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": order.total_price,
            "authority": authority,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response = response.json()
            if response['data'].get('code') == 100:
                order.is_paid = True
                order.save()
                return HttpResponse(response['data'].get('ref_id'))
            else:
                return HttpResponse(str(response['Status']))
        return HttpResponse(response)