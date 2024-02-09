from django.urls import path

from . import views
from .webhooks import stripe_webhook, yookassa_webhook


app_name = 'payment'

urlpatterns = [
    path("shipping/", views.shipping_view, name="shipping"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("complete-order/", views.complete_order, name="complete-order"),
    path('payment-success/', views.payment_success, name='payment-success'),
    path('payment-fail/', views.payment_fail, name='payment-fail'),
    # Webhooks
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
    path('webhook-yookassa/', yookassa_webhook, name='webhook-yookassa'),
    # Order PDF
    path("order/<int:order_id>/pdf/", views.admin_order_pdf, name="admin-order-pdf")
]
