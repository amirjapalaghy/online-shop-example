from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('detail', views.CartView.as_view(), name='cart-detail'),
    path('add/<int:pk>', views.AddToCartView.as_view(), name='add-cart'),
    path('delete/<str:id>', views.DeleteFromCartView.as_view(), name='delete-item'),
    path('order/<int:id>', views.OrderDetailView.as_view(), name='order-detail'),
    path('order/create', views.OrderCreateView.as_view(), name='order-create'),
    path('coupon/<int:id>', views.ApplyCouponView.as_view(), name='coupon'),
    path('send_request/<int:id>', views.SendRequest.as_view(), name='send_request'),
    path('verify', views.Verify.as_view(), name='verify_request'),
]