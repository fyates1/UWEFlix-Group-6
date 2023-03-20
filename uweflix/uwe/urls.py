from django.urls import path
from uwe import views

urlpatterns = [
    path('', views.loginView, name='loginView'),
    path('register/', views.register, name='register'),
    path('superuser/', views.superuser, name='superuser'),
    # path('create/',views.addClub, name="create"),
    # path('accountManager/', views.accountManager, name='accountManager'),
    # path('clubRepresentative/', views.clubRepresentative, name='clubRepresentative'),
    # path('customer/', views.customer, name='customer'),
    # path('cinemaManager/', views.cinemaManager, name='cinemaManager'),
]
