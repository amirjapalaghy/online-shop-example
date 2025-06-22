from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User, Otp


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('phone', 'password','email')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_admin','is_active')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','full_name', 'password1', 'password2')
        })
    )
    search_fields = ('phone',)
    ordering = ('phone',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

admin.site.register(Otp)