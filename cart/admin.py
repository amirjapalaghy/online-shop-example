from django.contrib import admin

from cart.models import Order, OrderItem, Coupon


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone', 'created_at', 'is_paid', )
    inlines = [OrderItemAdmin]
    list_filter = ('is_paid',)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'expire', 'quantity')
