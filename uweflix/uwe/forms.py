from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class RegisterForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    email = forms.CharField()

    class Meta:
        model = Users
        fields = ('username', 'password1', 'password2', 'email', 'is_accountManager', 'is_clubRepresentative', 'is_customer', 'is_cinemaManager')