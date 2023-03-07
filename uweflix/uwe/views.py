from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login
from .models import *

# Create your views here.

#REGISTER
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'uwe/register.html', {'form': form})
#LOGIN
def loginView(request):
    form=LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('superuser')
            elif user is not None and user.is_accountManager:
                login(request, user)
                return redirect('accountManager')
            elif user is not None and user.is_clubRepresentative:
                login(request, user)
                return redirect('clubRepresentative')
            elif user is not None and user.is_customer:
                login(request, user)
                return redirect('customer')
            elif user is not None and user.is_cinemaManager:
                login(request, user)
                return redirect('cinemaManager')
            else:
                return redirect('login')
        else:
            return redirect('login')
    return render(request, 'uwe/login.html', {'form': form})
    

#USERS
def superuser(request):
    return render(request, 'uwe/superuser.html')
def accountManager(request):
    return render(request, 'uwe/accountManager.html')
def clubRepresentative(request):
    return render(request, 'uwe/clubRepresentative.html')
def customer(request):
    return render(request, 'uwe/customer.html')
def cinemaManager(request):
    return render(request, 'uwe/cinemaManager.html')
