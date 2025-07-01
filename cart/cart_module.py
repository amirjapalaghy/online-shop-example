from django.shortcuts import get_object_or_404

from product.models import Product

CART_SESSION_ID = 'cart'


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            product = get_object_or_404(Product, id=int(item['product_id']))
            item['total'] = int(item['quantity']) * int(item['price'])
            item['product'] = product
            item['unique'] = self.unique_id_generator(product.id, item['size'], item['color'])
            yield item

    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def delete_cart(self, request):
        del request.session[CART_SESSION_ID]

    def total(self):
        cart = self.cart.values()
        total = sum(int(item['price']) * int(item['quantity']) for item in cart)
        return total

    def unique_id_generator(self, id, size, color):
        result = f'{id}-{size}-{color}'
        return result

    def add(self, product, quantity, color, size):
        unique_id = self.unique_id_generator(product.id, size, color)
        if unique_id not in self.cart:
            self.cart[unique_id] = {'product_id': product.id, 'quantity': 0, 'color': color, 'size': size,
                                    'price': str(product.price)}

        self.cart[unique_id]['quantity'] += int(quantity)
        self.save()

    def save(self):
        self.session.modified = True
