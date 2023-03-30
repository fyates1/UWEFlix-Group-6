from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login
from accounts.models import *
from django.urls import reverse
from django.forms.models import model_to_dict
import json
from datetime import date

# ----------------- Custom -----------------
def custom_authenticate(username, password):
    try:
        user = User.objects.get(username=username)
        if user.password == password:
            return user
    except User.DoesNotExist:
        pass
    return None

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

# ----------------- Views -----------------
# Contact Us Page
def contact_us(request):
    return render(request, 'uwe/contact_us.html')

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
        return redirect(reverse('login') + '?message=Registration Successful')
    else:
        return render(request, 'uwe/register.html', context)

#LOGIN
def login(request):
    print("Started")
    # Creates the UserForm based on if .POST exists
    form = LoginForm(request.POST or None)

    # Gets the message from the query parameters
    message = request.GET.get('message', None)

    # Gets all the variables to be passed into the page
    context = {
        'form': form,
        'message': message
    }

    # Checks if it's POST method
    if request.method == 'POST':
        print("is POST")
        # Gets the username and password inputs from the form
        username = request.POST['username']
        password = request.POST['password']

        print(f"username: {username} \npassword: {password}")

        # Testing code
        allUsers = User.objects.all()
        for user in allUsers:
            print(f"ID: {user.pk} | Username: {user.username} | Password: {user.password}")

        # Authenticates the user
        # user = authenticate(request, username=username, password=password)
        user = custom_authenticate(username=username, password=password)

        print(user)

        if user is not None:
            print("User is existing")
            # Convert the User object to a dictionary
            user_dict = model_to_dict(user)
            user_json = json.dumps(user_dict, cls=CustomJSONEncoder)
            print(user_json)
            request.session['user'] = user_json

            # Redirects to pages based on user type
            # TODO Make this redirect to pages based on the logged in user
            # if userType == "AM":
            #     return redirect(reverse("accountManager"))
            # elif userType == "CR":
            #     return redirect('clubRepresentative')
            # elif userType == "S":
            #     return redirect('customer')
            # elif  userType == "CM":
            #     return redirect('cinemaManager')
            # else:
            #     return redirect(reverse("login") + f'?message=Unkown User Type [{userType}]')

            print(f'first name: {user_dict["firstName"]} | last name: {user_dict["lastName"]}')
            return redirect(reverse('home') + f'?message={user_dict["firstName"]} {user_dict["lastName"]} is now logged in')
        else:
            print("User doesnt exist")
            # Adds an error message to the context and renders the page again
            context['message'] = 'Invalid username or password'
            return redirect(reverse("login") + f'?message=Invalid Login')

    print("age")
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
# def accountManager(request):
#     return render(request, 'accounts/index.html')
def clubRepresentative(request):
    return render(request, 'uwe/clubRepresentative.html')
def customer(request):
    return render(request, 'uwe/customer.html')
def cinemaManager(request):
    return render(request, 'uwe/cinemaManager.html')
