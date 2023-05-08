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
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path
from clubRep import views
from accounts.models import User

app_name = "clubRep"

urlpatterns = [
    path('addClub',views.addClub, {'user_required': True, 'user_types_required': User.UserType.CINEMAMANAGER}, name="addClub"),
    path("view",views.view_clubs, {'user_required': True, 'user_types_required': User.UserType.CINEMAMANAGER}, name="view"),
    path("show_club/<club_id>",views.view_club, {'user_required': True, 'user_types_required': User.UserType.CINEMAMANAGER}, name="showClub"),
    path("delete_club/<club_id>",views.delete_club, {'user_required': True, 'user_types_required': User.UserType.CINEMAMANAGER}, name="deleteClub"),
    path("update_club/<club_id>",views.update_club, {'user_required': True, 'user_types_required': User.UserType.CINEMAMANAGER}, name="updateClub"),
    path("settle",views.settle, {'user_required': True, 'user_types_required': User.UserType.CLUBREP,}, name="settle"),
    path('view/', views.view_clubs, {'user_required': True, 'user_types_required': User.UserType.CINEMAMANAGER}, name='view_clubs'),

    #path("delete_club/<club_id>",views.delete_club, name="deleteClub"),
    #path("show_club/<club_id>",views.show_club, name="showClub"),


]
