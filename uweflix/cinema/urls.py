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

app_name="cinema"
urlpatterns = [
    # screen
    path("add_screen",views.add_screen,name='add_screen'),
    path("list_screens",views.list_screens,name='list_screens'),
    path("show_screen/<screen_id>",views.show_screen,name="show_screen"),
    path("update_screen/<screen_id>",views.update_screen,name="update_screen"),
    path("delete_screen/<screen_id>",views.delete_screen,name="delete_screen"),

    # rows
    path("add_row",views.add_row,name='add_row'),
    path("list_rows",views.list_rows,name='list_rows'),
    path("show_row/<row_id>",views.show_row,name="show_row"),
    path("update_row/<row_id>",views.update_row,name="update_row"),
    path("delete_row/<row_id>",views.delete_row,name="delete_row"),

    # seats
    path("add_seat",views.add_seat,name='add_seat'),

    # Films
    path("list_films",views.list_films,name='film_listing'), # Update to table
    path("add_film",views.add_film,name='add_film'),
    path("update_film/<film_id>",views.update_film,name='update_film'),
    path("delete_film/<film_id>",views.delete_film,name="delete_film"),

    # Showings
    path("add_showing",views.add_showing,name="add_showing"),
    path("list_showings",views.list_showings,name="list_showings"),

    # Display

    path("show_film/<film_id>",views.show_film,name='show_film'),

    # D
    path("index",views.index,name="index"),
    path("display",views.display_films,name="list_films"),
    path("film_showing/<_id>",views.film_showing,name="film_showing"),
    path("cinema/booking/",views.booking_sheet,name="booking_sheet"),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)