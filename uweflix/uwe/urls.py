from django.urls import path
from uwe import views
from accounts import views as AMViews
from cinema import views as CViews
from accounts.models import User

urlpatterns = [
    # Home Page
    path('', CViews.display_films, name='home'),

    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('superuser', views.superuser, name='superuser'),
    # path('create/',views.addClub, name="create"),

    path('accounts', AMViews.index, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)}, name='accountManager'),

    path('contact_us', views.contact_us, name='contact_us'),
    path('my_tickets', views.my_tickets, name='my_tickets'),
    path('view_bookings', views.view_bookings, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)}, name='view_bookings'),
    path('cancel_bookings/<str:pk>/', views.cancel_bookings, {'user_required': True, 'user_types_required': (User.UserType.CINEMAMANAGER)}, name='cancel_bookings'),
]
