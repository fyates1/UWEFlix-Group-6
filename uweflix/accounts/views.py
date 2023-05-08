from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import *

# Create your views here.
def index(request, user_required=True, user_types_required=(User.UserType.ACCOUNTSMANAGER)):
    userList = User.objects.all() # List of all Users
    message = request.GET.get('message') # Get any message from previous pages

    context = {
        'userList': userList,
        'message': message,
    }

    return render(request, 'accounts/index.html', context)

def manageUser(request, userID, user_required=True, user_types_required=(User.UserType.ACCOUNTSMANAGER)):
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

def createUser(request, user_required=True, user_types_required=(User.UserType.ACCOUNTSMANAGER)):
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
