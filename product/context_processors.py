from .models import Category, Size, Color


def categories(request):
    roots = Category.objects.filter(parent=None).prefetch_related(
        'children__children__children'
    )
    return {'categories': roots}

def sizes(request):
    roots = Size.objects.all
    return {'sizes': roots}

def colors(request):
    roots = Color.objects.all
    return {'colors': roots}