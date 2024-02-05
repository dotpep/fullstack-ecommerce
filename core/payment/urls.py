from django.urls import path

from . import views


app_name = 'payment'

urlpatterns = [
    path("shipping/", views.shipping_view, name="shipping"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("complete-order/", views.complete_order, name="complete-order"),
    path('payment-success/', views.payment_success, name='payment-success'),
    path('payment-fail/', views.payment_fail, name='payment-fail'),
]
