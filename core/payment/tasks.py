from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

from .models import Order, ShippingAddress


# FIXME: celery worker tasks State in 'RECEIVED' not in 'SUCCESS' and there isn't sending that text to email
# FIXME: celery result (CELERY RESULTS app section in admin panel that uses library) - Task results doesn't shows any task but in flower it shows (may there is only shows tasks state of 'SUCCESS'.
@shared_task()
def send_order_confirmation_email(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order {order.id} payment Confirmation'
    receipent_data = ShippingAddress.objects.get(user=order.user)
    receipent_email = receipent_data.email
    message = f'Your order and payment has been confirmed. Your order number is {order.id}.'

    mail_to_send = send_mail(
        subject=subject, message=message, 
        from_email=settings.EMAIL_HOST_USER, 
        recipient_list=[receipent_email],
    )
    return mail_to_send