from django.urls import path
from uwe import views
from accounts import views as AMViews
from cinema import views as CViews

urlpatterns = [
    # Home Page
    path('', CViews.display_films, name='home'),

    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('superuser', views.superuser, name='superuser'),
    # path('create/',views.addClub, name="create"),

    path('accounts', AMViews.index, name='accountManager'),
    # TODO THE FOLLOWING NEEDS TO BE CHANGED BSAED ON THE HOME PAGES FOR EACH ROLE
    path('clubRepresentative', views.clubRepresentative, name='clubRepresentative'),
    path('customer', views.customer, name='customer'),
    path('cinemaManager', views.cinemaManager, name='cinemaManager'),
]