from django.shortcuts import render, get_object_or_404

from .models import Category, ProductProxy

# type hinting imports
from django.http import HttpRequest, HttpResponse
from django.db.models import SlugField

def products_view(request: HttpRequest) -> HttpResponse:
    products = ProductProxy.objects.all()
    context = {'products': products}
    return render(request, 'shop/products.html', context)


def product_detail_view(request: HttpRequest, slug: SlugField) -> HttpResponse:
    product = get_object_or_404(ProductProxy, slug=slug)
    context = {'product': product}
    return render(request, 'shop/product_detail.html', context)


def category_list(request: HttpRequest, slug: SlugField):
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.select_related('category').filter(category=category)
    context = {"category": category, "products": products}
    return render(request, 'shop/category_list.html', context)