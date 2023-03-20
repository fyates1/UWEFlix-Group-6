from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login
from accounts.models import *
from django.urls import reverse

# ----------------- Views -----------------
# Register page
def register(request):
    # Creates the UserForm based on if .POST exists
    form = UserForm(request.POST or None)

    # Gets all the variables to be passed into the page
    context = {
        "form": form
    }

    # Checks if it's POST method
    if request.method != 'POST':
        return render(request, 'uwe/register.html', context)

    # Checks if the form is valid
    if form.is_valid():
        # Saves the inputs to the database
        user = form.save()
        # Returns to the login page with a message
        return redirect(reverse('loginView') + '?message=Registration Successful')
    else:
        return render(request, 'uwe/register.html', context)

#LOGIN
def login(request):
    # TODO Needs to be tested

    # Creates the UserForm based on if .POST exists
    form = UserForm(request.POST or None)

    # Gets the message from the query parameters
    message = request.GET.get('message', None)

    # Gets all the variables to be passed into the page
    context = {
        'form': form,
        'message': message
    }

    # Checks if it's POST method
    if request.method == 'POST' and form.is_valid():
        # Gets the username and password inputs from the form
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # Authenticates the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Logs in the user and sets the user type in the session
            login(request, user)
            request.session['user_type'] = user.getUserType()

            # Redirects to the home page
            return redirect('home')
        else:
            # Adds an error message to the context and renders the page again
            context['error'] = 'Invalid username or password'
            return render(request, 'uwe/login.html', context)

    # Renders the page
    return render(request, 'uwe/login.html', context)

# def loginView(request):
#     form=LoginForm(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             print(username,password)
#             user = authenticate(username=username, password=password)
#             print(user)
#             if user is not None and user.is_superuser:
#                 login(request, user)
#                 return redirect('superuser')
#             elif user is not None and user.is_accountManager:
#                 login(request, user)
#                 return redirect('accountManager')
#             elif user is not None and user.is_clubRepresentative:
#                 login(request, user)
#                 return redirect('clubRepresentative')
#             elif user is not None and user.is_customer:
#                 login(request, user)
#                 return redirect('customer')
#             elif user is not None and user.is_cinemaManager:
#                 login(request, user)
#                 return redirect('cinemaManager')
#             else:
#                 return redirect('loginView')
#         else:
#             return redirect('loginView')
#     return render(request, 'uwe/login.html', {'form': form})

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
