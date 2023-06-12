from django.shortcuts import render
from django.views.generic import View

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem
from .tasks import order_created


class OrderCreateView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
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
            cart.clear()
            order_created.delay(order.id)
            return render(request, 'orders/order/created.html', {'order': order})

        return render(request, 'orders/order/create.html', {'cart': cart, "form": form})

    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html', {'cart': cart, "form": form})
