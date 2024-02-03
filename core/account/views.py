from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django_email_verification import send_email

from .forms import UserCreateForm

User = get_user_model()

def register_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')
            
            # Create new user
            user = User.objects.create_user(
                username=user_username, email=user_email, password=user_password
            )
            
            user.is_active = False
            
            send_email(user)
            
            return redirect('account:login')
    else:
        form = UserCreateForm()
    return render(request, 'account/registration/register.html', {'form': form}) 


def email_verification(request):
    pass
