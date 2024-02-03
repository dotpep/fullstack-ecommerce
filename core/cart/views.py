from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from shop.models import ProductProxy


def cart_view(request):
    return render(request, 'cart/cart-view.html')

def cart_add(request):
    pass

def cart_delete(request):
    pass

def cart_update(request):
    pass
