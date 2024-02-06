from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from decimal import Decimal

from cart.cart import Cart

from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress

from django.conf import settings

# stripe
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


# type hinting
from django.http import HttpRequest


# NOTE: I am using (login_url='account:login') because I am named it account app not default django login names that is accounts 
 # if I am name it accounts (default login required redirect), wouldn't write @login_required(login_url='account:login') instead just @login_required
 # This is mistake and you must consider to name your account app (accounts) read more about this: https://docs.djangoproject.com/en/5.0/topics/auth/default/
@login_required(login_url='account:login')
def shipping_view(request: HttpRequest):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping_address = None

    form = ShippingAddressForm(instance=shipping_address)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('payment:checkout')
    context = {'form': form}
    return render(request, 'shipping/shipping.html', context)

def checkout_view(request: HttpRequest):
    if request.user.is_authenticated:
        try:
            shipping_address = ShippingAddress.objects.get(user=request.user)
            context = {'shipping_address': shipping_address}
            return render(request, 'payment/checkout.html', context)
        except ShippingAddress.DoesNotExist:
            return redirect('payment:shipping')
    return render(request, 'payment/checkout.html')

def complete_order(request: HttpRequest):
    if request.method == 'POST':
        payment_type = request.POST.get('stripe-payment', 'yookassa-payment')

        name = request.POST.get('name')
        email = request.POST.get('email')
        street_address = request.POST.get('street_address')
        apartment_address = request.POST.get('apartment_address')
        country = request.POST.get('country')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        
        cart = Cart(request)
        total_price = cart.get_total_price()
        
        # FIXME: proccessed only one product instead 2... choosen in cart in payment method with stripe 
        match payment_type:
            case 'stripe-payment':
                shipping_address, _ = ShippingAddress.objects.get_or_create(
                    user=request.user,
                    defaults={
                        'full_name': name,
                        'email': email,
                        'street_address': street_address,
                        'apartment_address': apartment_address,
                        'country': country,
                        'city': city,
                        'zip_code': zip_code,
                    }
                )

                session_data = {
                    'mode': 'payment',
                    'success_url': request.build_absolute_uri(reverse('payment:payment-success')),
                    'cancel_url': request.build_absolute_uri(reverse('payment:payment-fail')),
                    'line_items': [],
                }
                
                if request.user.is_authenticated:
                    order = Order.objects.create(
                        user=request.user,
                        shipping_address=shipping_address,
                        total_price=total_price,
                    )
                    
                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item['product'],
                            price=item['price'],
                            quantity=item['qty'],
                            user=request.user,
                        )
                        session_data['line_items'].append({
                            'price_data': {
                                'unit_amount': int(item['price'] * Decimal(100)),
                                'currency': 'usd',
                                'product_data': {
                                    'name': item['product'],
                                },
                            },
                            'quantity': item['qty'],
                        })
                        
                        session = stripe.checkout.Session.create(**session_data)
                        return redirect(session.url, code=303)
                else:
                    order = Order.objects.create(
                        shipping_address=shipping_address,
                        total_price=total_price,
                    )
                    
                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item['product'],
                            price=item['price'],
                            quantity=item['qty'],
                        )


def payment_success(request: HttpRequest):
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]
    return render(request, 'payment/payment_success.html')


def payment_fail(request: HttpRequest):
    return render(request, 'payment/payment_fail.html')
