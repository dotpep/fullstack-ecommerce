from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput

# type hinting
from typing import Any

User = get_user_model()


class UserCreateForm(UserCreationForm):
    pass