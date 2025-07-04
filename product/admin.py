from django.contrib import admin

from product.models import Product, Color, Size, Information, Category


class InformationAdmin(admin.StackedInline):
    model = Information


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (InformationAdmin,)
    class Meta:
        fields = '__all__'
        list_display = ('name', 'price', 'image', 'created_at')
        ordering = ('modified_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Color)
admin.site.register(Size)
