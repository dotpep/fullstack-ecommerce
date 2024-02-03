from django.urls import path
from django.shortcuts import render

from . import views

app_name = 'account'

urlpatterns = [
    # Registration and Verification
    path('register', views.register_user, name='register'),
    path(
        route='email-verification-sent/',
        view=lambda request: render(request, 'account/email/email_verification_sent.html'),
        name='email-verification-sent'
    ),
]
