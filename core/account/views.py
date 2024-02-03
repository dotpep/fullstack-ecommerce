from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django_email_verification import send_email

from .forms import UserCreateForm

User = get_user_model()

def register(request):
    pass
