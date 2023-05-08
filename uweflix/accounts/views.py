from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import *
from cinema.models import Booking
from datetime import timedelta, datetime

# Create your views here.
def index(request, user_required=True, user_types_required=(User.UserType.CINEMAMANAGER)):
    userList = User.objects.all() # List of all Users
    message = request.GET.get('message') # Get any message from previous pages

    context = {
        'userList': userList,
        'message': message,
    }

    return render(request, 'accounts/index.html', context)

def manageUser(request, userID, user_required=True, user_types_required=(User.UserType.CINEMAMANAGER)):
    user = get_object_or_404(User, pk=userID)
    userForm = UserForm(request.POST or None, instance=user)

    context = {
        'user': user,
        'userForm': userForm
    }

    # When used to render page
    if request.method != 'POST':
        return render(request, 'accounts/manageUser.html', context)

    if request.POST.get('submit', False):# If the update button is pressed
        if userForm.is_valid():
            userForm.save()
            return redirect(reverse('accounts:index') + '?message=Update Successful')

        else:
            return render(request, 'accounts/manageUser.html', context)

    elif request.POST.get('delete', False): # If the delete button is pressed
        user.delete()
        return redirect(reverse('accounts:index') + '?message=Entry Deleted')

def createUser(request, user_required=True, user_types_required=(User.UserType.CINEMAMANAGER)):
    userForm = UserForm(request.POST or None)

    context = {
        "userForm": userForm
    }

    if request.method != 'POST':
        return render(request, 'accounts/createUser.html', context)

    if userForm.is_valid():
        userForm.save()
        return redirect(reverse('accounts:index') + '?message=New User Created')
    else:
        return render(request, 'accounts/createUser.html', context)

def getPaymentHistory(request, user_required=True, user_types_required=(User.UserType.ACCOUNTSMANAGER)):
    form = UserFilterForm(request.POST or None)
    timeFrom = request.POST.get('timeFrom', None) if request.method == 'POST' else None
    userFilter = None

    if form.is_valid():
        userFilter = form.cleaned_data['user']

    # Filter bookings based on the criteria
    paymentList = Booking.objects.all()

    if timeFrom and timeFrom.strip():
        timeFrom = datetime.strptime(timeFrom, '%Y-%m-%d')
        timeTo = timeFrom + timedelta(days=30)
        paymentList = paymentList.filter(purchase_date__range=(timeFrom, timeTo))

    if userFilter is not None:
        paymentList = paymentList.filter(user=userFilter)

    context = {
        'form': form,
        'paymentList': paymentList,
    }

    return render(request, 'accounts/paymentHistory.html', context)

