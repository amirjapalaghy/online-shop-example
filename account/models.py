from enum import unique

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .managers import UserManager

# class User(AbstractBaseUser, PermissionsMixin):

class User(AbstractBaseUser):

    email = models.EmailField(
        max_length=255, unique=True,
        verbose_name='email address',
        null=True, blank=True
    )
    full_name = models.CharField(max_length=255, verbose_name='full name')
    phone = models.CharField(max_length=255, unique=True, verbose_name='phone number')
    is_active = models.BooleanField(default=True, verbose_name='active')
    is_admin = models.BooleanField(default=False, verbose_name='admin')

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Otp(models.Model):
    phone = models.CharField(max_length=11, verbose_name='phone number')
    code = models.SmallIntegerField(verbose_name='code')
    expires= models.DateTimeField(verbose_name='expires', auto_now_add=True)

    def __str__(self):
        return self.phone