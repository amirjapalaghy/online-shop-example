import os
import uuid

from django.db import models
from django.utils import timezone


def _get_avatar_upload_path(instance, filename):
    now = timezone.now()
    base_path = 'avatar'
    new_filename = str(uuid.uuid4())
    ext = os.path.splitext(filename)[1]
    path = os.path.join(base_path, now.strftime("%Y/%m"), f'{new_filename}{ext}')
    return path


class Product(models.Model):
    name = models.CharField(max_length=100)
    # price = models.DecimalField(decimal_places=3, max_digits=10)
    price = models.IntegerField()
    image = models.ImageField(upload_to=_get_avatar_upload_path, null=True, blank=True)
    discount = models.IntegerField(default=0)
    short_description = models.TextField(max_length=300)
    description = models.TextField()
    additional_info = models.TextField(null=True, blank=True)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)
    size = models.ManyToManyField('Size', related_name='products', blank=True)
    color = models.ManyToManyField('Color', related_name='products')

    def __str__(self):
        return f'{self.name} -- {self.price}'


class Size(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='information', null=True)
    text = models.TextField()

    def __str__(self):
        return self.text[:20]