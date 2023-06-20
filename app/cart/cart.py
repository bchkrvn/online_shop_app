from _decimal import Decimal

from django.conf import settings

from coupons.models import Coupon
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
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product: Product, quantity=1, override_quantity=False):
        """
        Add product to cart or update its quantity
        """
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
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

    @property
    def coupon(self) -> Coupon or None:
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                return None

    def get_discount(self):
        if self.coupon:
            return Decimal(round((self.coupon.discount / Decimal(100)) * self.get_total_price(), 2))
        return Decimal(0)

    def get_total_price_with_discount(self):
        return self.get_total_price() - self.get_discount()
