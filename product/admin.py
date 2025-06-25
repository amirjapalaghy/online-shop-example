from django.contrib import admin

from product.models import Product, Color, Size, Information


class InformationAdmin(admin.StackedInline):
    model = Information


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (InformationAdmin,)
    class Meta:
        fields = '__all__'
        list_display = ('name', 'price', 'image', 'created_at')
        ordering = ('modified_at',)


admin.site.register(Color)
admin.site.register(Size)
