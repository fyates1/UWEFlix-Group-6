from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login
from accounts.models import *
from django.urls import reverse
from django.forms.models import model_to_dict
import json
from datetime import date
from cinema.models import *

from django.db.models import Q

#-------------Email------------------
from django.conf import settings
from django.core.mail import send_mail

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

def view_bookings(request, user_required: True, user_types_required: (User.UserType.CINEMAMANAGER)):
    message = request.GET.get('message')
    search_query = ""

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    data = Booking.objects.filter(
        Q(bookingID__icontains=search_query)
    )

    context = {
        'data': data,
        'search_query': search_query,
        'message': message,
    }
    return render(request, 'uwe/view_bookings.html', context)

def cancel_bookings(request, pk, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    data = Booking.objects.get(bookingID=pk)

    if request.method == 'POST':
        data.delete()
        return redirect(reverse('view_bookings') + '?message=The booking was deleted!')
    context = {
        'data' : data,
    }
    return render(request, 'uwe/cancel_bookings.html', context)


def my_tickets(request):
    user = User.objects.get(id=request.session['id'])
    data = Booking.objects.filter(user=user)

    #data  = Booking.objects.get(user = user)
    context = {
        'data' : data
    }
    return render(request, 'uwe/my_tickets.html', context)


# Register page
def register(request):
    # Creates the UserForm based on if .POST exists
    # form = UserForm(request.POST or None)
    form = RegisterForm(request.POST or None)

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
        email = [form.cleaned_data.get('userEmail')]
        email_subject = 'Registration Confirmation'
        email_message = 'Congratulations, \n\nYou have successfully created an account at UWEFLIX. \n\nWe hope you enjoy it!\n\n\nKind regards,\nUWEFlix Team.'
        user.save()
        send_mail(email_subject, email_message, settings.CONTACT_EMAIL, email)
        # Returns to the login page with a message
        return redirect(reverse('login') + '?message=Registration Successful')
    else:
        return render(request, 'uwe/register.html', context)

#LOGIN
def login(request):
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
        # Gets the username and password inputs from the form
        username = request.POST['username']
        password = request.POST['password']

        # Authenticates the user
        # user = authenticate(request, username=username, password=password)
        user = custom_authenticate(username=username, password=password)

        if user is not None:
            # Checks if the user's account has been activated
            if user.activated == False:
                # Redirect to home and say the account needs to be activated
                return redirect(reverse("login") + f'?message=Account has not been activated')

            # Convert the User object to a dictionary
            user_dict = model_to_dict(user)
            # user_json = json.dumps(user_dict, cls=CustomJSONEncoder)
            # request.session['user'] = user_json

            for key, value in user_dict.items():
                request.session[key] = json.dumps(value, cls=CustomJSONEncoder)
                # request.session[key] = str(value)

            return redirect(reverse('home') + f'?message={user_dict["firstName"]} {user_dict["lastName"]} is now logged in')
        else:
            # Adds an error message to the context and renders the page again
            context['message'] = 'Invalid username or password'
            return redirect(reverse("login") + f'?message=Invalid Login')

    # Renders the page
    return render(request, 'uwe/login.html', context)

def logout(request):
    print(request.session)

    if 'id' in request.session:
        # del request.session['user']
        request.session.flush()

    return redirect(reverse('login'))

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
