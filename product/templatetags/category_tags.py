from django import template
from product.models import Category

register = template.Library()

@register.inclusion_tag('product/category_tree.html')
def render_category(category):
    return {'category': category}