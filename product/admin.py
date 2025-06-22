from django.contrib import admin

from product.models import Product, Color, Size


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product
        fields = '__all__'
        list_display = ('name', 'price', 'image', 'created_at')
        ordering = ('modified_at',)


admin.site.register(Color)
admin.site.register(Size)
