"""uweflix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from . import views
from .models import User

app_name = "accounts"

urlpatterns = [
    # Accounts Index
    path('', views.index, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)}, name='index'),

    # User Creation Page
    path('user/create/', views.createUser, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)}, name="createUser"),

    # User Manage page
    path('user/<int:userID>/', views.manageUser, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)}, name="manageUser"),

    # Payment History Page
    path('payments/', views.getPaymentHistory, {'user_required': True, 'user_types_required': (User.UserType.ACCOUNTSMANAGER)}, name='getPaymentHistory')
]
