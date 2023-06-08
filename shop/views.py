from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from shop.models import Product, Category


class ProductsList(ListView):
    def get(self, request, category_slug=None, *args, **kwargs):
        category = None
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        categories = Category.objects.all()

        return render(request,
                      'shop/product/list.html',
                      {'category': category,
                       'categories': categories,
                       'products': products})


class ProductDetail(DetailView):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product,
                                    id=kwargs['id'],
                                    slug=kwargs['slug'],
                                    available=True)
        return render(request,
                      'shop/product/detail.html',
                      {'product': product})
