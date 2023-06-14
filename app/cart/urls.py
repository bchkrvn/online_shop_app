from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', login_required(views.CartDetailView.as_view()), name='cart_detail'),
    path('add/<int:product_id>/', login_required(views.CartAddView.as_view()), name='cart_add'),
    path('remove/<int:product_id>/', login_required(views.CartRemoveView.as_view()), name='cart_remove')
]
