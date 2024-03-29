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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from accounts.models import User

app_name="cinema"
urlpatterns = [
    # screen
    path("add_screen",views.add_screen, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name='add_screen'),
    path("list_screens",views.list_screens, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name='list_screens'),
    path("show_screen/<screen_id>",views.show_screen, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name="show_screen"),
    path("update_screen/<screen_id>",views.update_screen, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name="update_screen"),
    path("delete_screen/<screen_id>",views.delete_screen, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name="delete_screen"),

    # rows
    path("add_row",views.add_row, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name='add_row'),
    path("list_rows",views.list_rows, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name='list_rows'),
    path("show_row/<row_id>",views.show_row, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name="show_row"),
    path("update_row/<row_id>",views.update_row, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name="update_row"),
    path("delete_row/<row_id>",views.delete_row, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name="delete_row"),

    # seats
    path("add_seat",views.add_seat, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name='add_seat'),

    # Films
    path("list_films",views.list_films, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name='film_listing'), # Update to table
    path("add_film",views.add_film, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name='add_film'),
    path("update_film/<film_id>",views.update_film, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name='update_film'),
    path("delete_film/<film_id>",views.delete_film, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name="delete_film"),

    # Showings
    path("add_showing",views.add_showing, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name="add_showing"),
    path("list_showings",views.list_showings, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)},name="list_showings"),

    # Display

    path("show_film/<film_id>",views.show_film,name='show_film'),

    # D
    path("index",views.index,name="index"),
    path("display",views.display_films,name="list_films"),
    path("film_showing/<_id>",views.film_showing,name="film_showing"),
    path("delete_showing/<showing_id>",views.delete_showing,name="delete_showing"),
    path("update_showing/<showing_id>",views.update_showing,name="update_showing"),


    # booking
    path("booking_film/",views.booking_sheet,name="booking_sheet"),
    path("booking_film/<showing_id>",views.book_showing,{'user_required': True, 'user_types_required': (User.UserType.STUDENT)},name="create_booking"), # student
    path("booking_film_cr/<showing_id>",views.book_showing_cr,{'user_required': True, 'user_types_required': (User.UserType.CLUBREP)},name="create_booking_cr"), # club rep
    path("settling_balance",views.settling_balance,{'user_required': True, 'user_types_required': (User.UserType.STUDENT,User.UserType.CLUBREP)},name="settling_balance"), # settling balance
    path("booking_film_guest/<showing_id>",views.book_showing_guest,name="create_booking_guest"), # guest
    path("booking_film_AM_CM/<showing_id>",views.book_showing_AM_CM,{'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER,User.UserType.ACCOUNTSMANAGER)},name="create_booking_AM_CM"),

    # Activating Accounts
    path("activate", views.activate_accounts, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)}, name="activate_accounts_default"),
    path("activate/", views.activate_accounts, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)}, name="activate_accounts_default"),
    path("activate/<int:userID>", views.activate_accounts, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)}, name="activate_accounts"),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)