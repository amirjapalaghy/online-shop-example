from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('', views.ProductListView.as_view(), name='product-list'),
    path('navbar', views.NavbarPartialView.as_view(), name='navbar'),
]