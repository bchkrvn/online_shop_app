from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order
from shop.recommender import Recommender
from .tasks import order_created


class OrderCreateView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.user = request.user
            order.save()

            for item in cart:
                product = item['product']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item['price'],
                    quantity=item['quantity'],
                )
                product.quantity -= item['quantity']
                product.save()

            Recommender().products_bought([item['product'] for item in cart])
            cart.clear()
            request.session['coupon_id'] = None
            order_created.delay(order.id)

            return render(request, 'orders/order/created.html', {'new_order': order})

        return render(request, 'orders/order/create.html', {'cart': cart, "form": form})

    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html', {'cart': cart, "form": form})


class OrderDetailView(View):
    def get(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id)
        items = OrderItem.objects.filter(order=order)
        return render(request, 'orders/order/detail.html', {'order': order, "items": items})
