from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.OrderCreateFormView.as_view(), name='order_create'),
]
