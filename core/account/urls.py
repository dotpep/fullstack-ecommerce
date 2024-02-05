from django.urls import path
from django.shortcuts import render

from . import views

app_name = 'account'

urlpatterns = [
    # Registration and Verification
    path('register/', views.register_user, name='register'),
    path(
        route='email-verification-sent/',
        view=lambda request: render(request, 'account/email/email_verification_sent.html'),
        name='email-verification-sent'
    ),
    # Login and Logout
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard_user, name='dashboard'),
    path('profile-management/', views.profile_user_management, name='profile-management'),
    path('delete-user/', views.delete_user, name='delete-user'),
    
]
