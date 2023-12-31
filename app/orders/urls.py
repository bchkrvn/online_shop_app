from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', login_required(views.OrderCreateView.as_view()), name='order_create'),
    path('<int:order_id>', login_required(views.OrderDetailView.as_view()), name='order_detail'),
]
