from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, ListView

from product.models import Product, Category


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_details.html'

class NavbarPartialView(TemplateView):
    template_name = 'includes/navbar.html'

class ProductListView(ListView):
    template_name = 'product/product_list.html'
    queryset = Product.objects.all

    def get_context_data(self, **kwargs):
        request = self.request
        colors = request.GET.getlist('color')
        sizes = request.GET.getlist('size')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        queryset = Product.objects.all
        if colors:
            queryset = Product.objects.filter(color__name__in=colors).distinct()

        if sizes:
            queryset = Product.objects.filter(size__name__in=sizes).distinct()

        if min_price and max_price:
            queryset = Product.objects.filter(price__gte=min_price, price__lte=max_price).distinct()

        context = super(ProductListView, self).get_context_data(**kwargs)
        context['object_list'] = queryset
        return context
