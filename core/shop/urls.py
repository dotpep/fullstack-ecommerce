from django.urls import path

from .views import ProductListView, product_detail_view, category_list


app_name = 'shop'

urlpatterns = [
    #path('', products_view, name='products'),
    path('', ProductListView.as_view(), name='products'),
    path('<slug:slug>/', product_detail_view, name='product-detail'),
    path('search/<slug:slug>/', category_list, name='category-list'),
]
