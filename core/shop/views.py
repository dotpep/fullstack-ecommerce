from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Category, ProductProxy

# type hinting imports
from django.http import HttpRequest, HttpResponse
from django.db.models import SlugField


#def products_view(request: HttpRequest) -> HttpResponse:
#    products = ProductProxy.objects.all()
#    context = {'products': products}
#    return render(request, 'shop/products.html', context)
class ProductListView(ListView):
    model = ProductProxy
    context_object_name = "products"
    paginate_by = 15
    
    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return "shop/components/product_list.html"
        return "shop/products.html"


def product_detail_view(request: HttpRequest, slug: SlugField) -> HttpResponse:
    product = get_object_or_404(ProductProxy, slug=slug)
    context = {'product': product}
    return render(request, 'shop/product_detail.html', context)


def category_list(request: HttpRequest, slug: SlugField):
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.select_related('category').filter(category=category)
    context = {"category": category, "products": products}
    return render(request, 'shop/category_list.html', context)


def search_products():
    pass