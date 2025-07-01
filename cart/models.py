from importlib.metadata import requires

from django.db import models

from account.models import User
from product.models import Product, Size, Color


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    address = models.CharField(max_length=350)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    total_price = models.IntegerField(default=0)

    def __str__(self):
        return self.user.phone


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_items')
    size = models.CharField(max_length=5, null=True, blank=True)
    color = models.CharField(max_length=5, null=True, blank=True)
    quantity = models.SmallIntegerField(default=1)
    price = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product.name


class Coupon(models.Model):
    code = models.CharField(max_length=6, unique=True)
    quantity = models.SmallIntegerField(default=1)
    discount = models.IntegerField(default=0)
    expire = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code

