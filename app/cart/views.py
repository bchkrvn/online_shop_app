from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from cart.cart import Cart
from cart.forms import CartAddProductForm
from shop.models import Product


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
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={
                'quantity': item['quantity'],
                'override': True
            })
        return render(request, 'cart/detail.html', {'cart': cart})
