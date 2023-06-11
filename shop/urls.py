from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', login_required(views.ProductsList.as_view()), name='product_list'),
    path('<slug:category_slug>/', login_required(views.ProductsList.as_view()), name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', login_required(views.ProductDetail.as_view()), name='product_detail'),
]
