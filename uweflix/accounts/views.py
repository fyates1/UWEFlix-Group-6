from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    userList = User.objects.all() # List of all Users
    message = request.GET.get('message') # Get any message from previous pages

    context = {
        'userList': userList,
        'message': message,
    }

    return render(request, 'accounts/index.html', context)