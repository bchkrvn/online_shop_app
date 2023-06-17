from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from cart.cart import Cart
from cart.forms import CartAddProductForm
from shop.models import Product
from shop.recommender import Recommender
from coupons.forms import CouponApplyForm


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            if cd['quantity'] > product.quantity:
                cd['quantity'] = product.quantity
            cart.add(product=product,
                     quantity=cd['quantity'],
                     override_quantity=cd['override'])

        return redirect('cart:cart_detail')


class CartRemoveView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart:cart_detail')


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        cart_products = []

        for item in cart:
            cart_products.append(item['product'])
            item['update_quantity_form'] = CartAddProductForm(initial={
                'quantity': item['quantity'],
                'override': True
            })

        if cart_products:
            recommended_products = Recommender().submit_products_for(cart_products, max_results=4)
        else:
            recommended_products = []

        coupon_apply_form = CouponApplyForm()
        return render(request, 'cart/detail.html', {'cart': cart,
                                                    'coupon_apply_form': coupon_apply_form,
                                                    'recommended_products': recommended_products})
