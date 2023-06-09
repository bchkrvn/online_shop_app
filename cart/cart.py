from _decimal import Decimal

from django.conf import settings

from shop.models import Product


class Cart:
    """
    Shopping cart
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product, quantity=1, override_quantity=False):
        """
        Add product to cart or update its quantity
        """
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id][quantity] = quantity
        else:
            self.cart[product_id][quantity] += quantity
        self.save()

    def save(self):
        """
        Mark session as "modified"
        """
        self.session.modified = True

    def remove(self, product: Product):
        """
        Delete product from cart
        """
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart
        and get the products from the DB
        """

        products_id = self.cart.keys()
        products = Product.objects.filter(id__in=products_id)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Get all quantity items in cart
        """
        return sum([item['quantity'] for item in self.cart.values()])

    def get_total_price(self):
        return sum([Decimal(item['price']) * item['quantity'] for item in self.cart.values()])

    def clear(self):
        """
        Delete cart from session
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
