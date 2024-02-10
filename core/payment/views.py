from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.urls import reverse
from decimal import Decimal
import uuid
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.templatetags.static import static
import weasyprint

from cart.cart import Cart

from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress

from django.conf import settings

# payment api
import stripe
from yookassa import Payment, Configuration

# type hinting
from django.http import HttpRequest


# Stripe configuration
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

# Yookassa configuration
Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


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
        
        # TODO: refactor this match case payment type stripe and yookassa to modular and dry

        match payment_type:
            # Stripe
            case "stripe-payment":
                
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
                    
                    session_data['client_reference_id'] = order.id
                    
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
                    
                    session_data['client_reference_id'] = order.id
                    
                    session = stripe.checkout.Session.create(**session_data)
                    return redirect(session.url, code=303)
                
                        
            # Yookassa
            # FIXME: yookassa cannot change status of payment (is_paid)
            case "yookassa-payment":
                idempotence_key = uuid.uuid4()
                
                currency = 'RUB'
                description = 'Товар в корзине'
                payment = Payment.create({
                    "amount": {
                        "value": str(total_price * 93),
                        "currency": currency,
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": request.build_absolute_uri(reverse('payment:payment-success')),
                    },
                    "capture": True,
                    "test": True,
                    "description": description,
                }, idempotence_key)
                
                confirmation_url = payment.confirmation.confirmation_url
                
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
                    
                    return redirect(confirmation_url)
                
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

            case _ :
                return JsonResponse({'error': 'Unsupported payment type'})

    return JsonResponse({'error': 'Invalid request'})


def payment_success(request: HttpRequest):
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]
    return render(request, 'payment/payment_success.html')


def payment_fail(request: HttpRequest):
    return render(request, 'payment/payment_fail.html')


@staff_member_required
def admin_order_pdf(request: HttpRequest, order_id):
    try:
        order = Order.objects.select_related('user', 'shipping_address').get(id=order_id)
    except Order.DoesNotExist:
        raise Http404("Order does't exits or find")
    html = render_to_string('payment/order/pdf/pdf_invoice.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Dispposition'] = f"filename=order_{order.id}.pdf"
    css_path = static('payment/css/pdf.css').lstrip('/')
    # css_path = 'static/payment/css/pdf.css'
    stylesheets = [weasyprint.CSS(css_path)]
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=stylesheets)
    return response
