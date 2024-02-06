from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django_email_verification import send_email

from .forms import UserCreateForm, UserLoginForm, UserUpdateForm

# type hinting
from django.http import HttpRequest


User = get_user_model()

# FIXME: fix and refactor account app, implement additional functionality

# NOTE: accounts templates stored in (that you can use if you name your app accounts): django\contrib\admin\templates\registration
 # but I am make custom template for password resetting

# Register new user
def register_user(request: HttpRequest):
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
            
            return redirect('/account/email-verification-sent/')
    else:
        form = UserCreateForm()
    return render(request, 'account/registration/register.html', {'form': form}) 


def login_user(request: HttpRequest):
    form = UserLoginForm()
    
    if request.user.is_authenticated:
        return redirect('shop:products')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request=request, user=user)
            return redirect('account:dashboard')
        else:
            messages.info(request, "Username or Password is incorrect")
            return redirect('account:login')

    context = {'form': form}
    return render(request, 'account/login/login.html', context)


def logout_user(request: HttpRequest):
    logout(request)
    return redirect('shop:products')


# Dashboard
@login_required(login_url='account:login')
def dashboard_user(request: HttpRequest):
    return render(request, 'account/dashboard/dashboard.html')


@login_required(login_url='account:login')
def profile_user_management(request: HttpRequest):

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('account:dashboard')
    else:
        form = UserUpdateForm(instance=request.user)
        
    context = {'form': form}
    return render(request, 'account/dashboard/profile_management.html', context)
    


@login_required(login_url='account:login')
def delete_user(request: HttpRequest):
    user = User.objects.filter(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        return redirect('shop:products')
    
    return render(request, 'account/dashboard/account_delete.html')
