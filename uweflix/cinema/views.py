from django.shortcuts import render,redirect
from django.urls import reverse
#from .forms import ScreenForm,RowForm,SeatForm,FilmForm,ShowingForm,BookingForm, BookingForm_cr
from django.contrib import messages
from .forms import *
from .models import screen,row,film,showing,Booking
from accounts.models import User, UserForm
from django.http import HttpResponseRedirect
from django.db.models.deletion import RestrictedError
from django.shortcuts import get_list_or_404, get_object_or_404
import requests
from json import JSONDecodeError
import pandas as pd
from datetime import datetime, timedelta
from django.db.models import Q

class CinemaManager():
    #All data functions related to getting data from the database are here
    
    #Get a list of screens
    def get_screenList():
        List = screen.objects.all()
        return List
    #Get a screen from ID
    def get_screen(id):
        return screen.objects.get(pk=id)
    #Get a list of rows from database
    def get_rowList():
        List = row.objects.all()
        return List
    #Get a row from ID
    def get_row(id):
        return row.objects.get(pk=id)
    #Get a film from ID
    def get_film(id):
        return film.objects.get(pk=id)
    #Get a showing from ID
    def get_showing(id):
        return showing.objects.get(pk=id)

# Function to authenticate new registrations
def activate_accounts(request, userID = None, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    # Gets all unactivated accounts
    unactivatedAccounts = User.objects.filter(activated=False)
    message = request.GET.get('message')

    if userID != None:
        user = User.objects.get(id=userID)
        userForm = UserForm(request.POST or None, instance=user)
    else:
        # This will be none when no account is selected because the form wont even be visible at that time
        user = None
        userForm = None # TODO Check if this can be called like a form without erroring OTHERWISE this will get a blank form

    context = {
        'accounts': unactivatedAccounts,
        'message': message,
        'user': user,
        'userForm': userForm
    }

    if request.method != 'POST':
        return render(request, "cinema/unactivated_accounts.html", context)

    if request.POST.get('deny', False): # If the  button is pressed
        user.delete()
        return redirect(reverse('cinema:activate_accounts_default') + '?message=User Deleted')

    elif request.POST.get('approve', False): # If the submit button is pressed
        user.activated = True
        user.save()
        return redirect(reverse('cinema:activate_accounts_default') + '?message=User Account Activated')

#Function to add a screen to the system
def add_screen(request, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
        submitted = False
        if request.method == "POST":
            form = ScreenForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/cinema/add_screen?submitted=True")
        else:
            form = ScreenForm
            if "submitted" in request.GET:
                submitted = True
        return render(request,"cinema/add_screen.html",{"form":form ,"submitted":submitted})

#Function to add a row to a screen 
def add_row(request, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
        submitted = False
        if request.method == "POST":
            form = RowForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/cinema/add_row?submitted=True")
        else:
            form = RowForm
            if "submitted" in request.GET:
                submitted = True
        return render(request,"cinema/add_row.html",{"form":form ,"submitted":submitted})

#Function to display film list
def list_screens(request):
    screen_list = CinemaManager.get_screenList()
    return render(request,"cinema/screens.html",{"screen_list":screen_list,})

#Function to display row list
def list_rows(request):
    row_list = row.objects.all()
    return render(request,"cinema/rows.html",{"row_list":row_list,})

#Function to display data on a screen
def show_screen(request,screen_id, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    Screen = CinemaManager.get_screen(screen_id)
    return render(request,"cinema/show_screen.html",{"screen":Screen})

#Function to show data of a row
def show_row(request,row_id, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    Row = CinemaManager.get_row(row_id)
    return render(request,"cinema/show_row.html",{"row":Row})

#Function to update a screen through a form
def update_screen(request, screen_id, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    Screen = CinemaManager.get_screen(screen_id)
    form = ScreenForm(request.POST or None,instance=Screen)
    if form.is_valid():
            form.save()
            return redirect('list_screens')
    return render(request,"cinema/update_screen.html",{"screen":Screen, "form":form})

#Function to update a row through a form
def update_row(request, row_id, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    Row = CinemaManager.get_row(row_id)
    form = RowForm(request.POST or None,instance=Row)
    if form.is_valid():
            form.save()
            return redirect('list_rows')
    return render(request,"cinema/update_row.html",{"row":Row, "form":form})

#Function to delete a screen through a form
def delete_screen(request,screen_id, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    Screen = CinemaManager.get_screen(screen_id)
    Screen.delete()
    return redirect("list_screens")

#Function to delete a row through a form
def delete_row(request,row_id, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    Row = CinemaManager.get_row(row_id)
    Row.delete()
    return redirect("list_rows")

#Function to add a seat through a form
def add_seat(request, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
        submitted = False
        if request.method == "POST":
            form = SeatForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/cinema/add_seat?submitted=True")
        else:
            form = SeatForm
            if "submitted" in request.GET:
                submitted = True
        return render(request,"cinema/add_seat.html",{"form":form ,"submitted":submitted})

#Function to add a film through a form
def add_film(request, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
        submitted = False
        page=1
        movies= movie_api_request(page) # Gets most popular movies via api request
        if request.method == "POST":
            form = FilmForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/cinema/add_film?submitted=True")
        else:
            form = FilmForm
            if "submitted" in request.GET:
                submitted = True
        return render(request,"cinema/add_film.html",{"form":form ,"submitted":submitted,"movies":movies})

#Lists films in our cinema
def list_films(request):
    film_listing = film.objects.all()
    return render(request,"cinema/films.html",{"film_listing":film_listing})

#Shows data stored about a film
def show_film(request,film_id):
    film = CinemaManager.get_film(film_id)
    return render(request,"cinema/show_film.html",{"film":film})

#Function to update film data through a form
def update_film(request, film_id, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    Film = CinemaManager.get_film(film_id)
    form = FilmForm(request.POST or None,instance=Film)
    if form.is_valid():
            form.save()
            return redirect('cinema:list_films')
    return render(request,"cinema/update_film.html",{"film":Film, "form":form})

#Function to delete a film
def delete_film(request,film_id, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    Film= CinemaManager.get_film(film_id)
    try:
        Film.delete()
        return redirect("cinema:list_films")
    except RestrictedError:
        message = "Sorry cant delete a film that has shwoings!"
        film_listing = film.objects.all()
        return render(request,"cinema/films.html",{"film_listing":film_listing,"message":message})

#Function to add a showing via form
def add_showing(request, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
        submitted = False
        if request.method == "POST":
            form = ShowingForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/cinema/add_showing?submitted=True")
        else:
            form = ShowingForm
            if "submitted" in request.GET:
                submitted = True
        return render(request,"cinema/add_showing.html",{"form":form ,"submitted":submitted})


# Showing display for cinema manager to add crud to 
def list_showings(request, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    startdate= datetime.today()
    enddate = startdate + timedelta(days=365)
    showing_list = showing.objects.filter(date__range=[startdate, enddate])
    return render(request,"cinema/showings.html",{"showing_list":showing_list})

#Form to delete a showing
def delete_showing(request,showing_id, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    Showing = CinemaManager.get_showing(showing_id)
    Showing.delete()
    return redirect("cinema:list_showings")

#Form to update a showing
def update_showing(request, showing_id, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    Showing = CinemaManager.get_showing(showing_id)
    form = ShowingForm(request.POST or None,instance=Showing)
    if form.is_valid():
            form.save()
            return redirect('cinema:list_showings')
    return render(request,"cinema/update_showing.html",{"showing":Showing, "form":form})

# Not used currently. Although keep
def index(request):
    index = film.objects.all()
    return render(request,"cinema/index.html",{"index":index})

# Main display screen
def display_films(request):
    message = request.GET.get('message')

    film_list = film.objects.all()
    return render(request,"cinema/display_films.html",{"film_list":film_list, "message": message})

# Film details when clicking
def film_showing(request, _id):
    current_time = timezone.now()
    film_showings = film.objects.get(id=_id)
    showings = showing.objects.filter(Q(date__gte=datetime.today()))
    filtered_showings = []
    for x in showings:
        if x.date == datetime.today() and x.film == film_showings:
            if x.time < current_time:
                filtered_showings.append(x)
        elif x.film == film_showings:
            filtered_showings.append(x)

            

    return render(request,"cinema/film_showing.html",{"film_showings":filtered_showings})

# Booking 
def booking_sheet(request):
    form = BookingForm()
    return render(request,'cinema/film_showing.html', {'form': form })


# TICKET PRICES 
adult_ticket_price = 8
student_ticket_price = 8
child_ticket_price = 5
cr_ticket_price = 6.8

# booking for Student

def book_showing(request, showing_id, user_required = True , user_types_required=(User.UserType.STUDENT)):
    showing = CinemaManager.get_showing(showing_id)


    # for key,value in request.session.items():
    #     print ('{} =>{}'.format(key,value))


    if request.method == 'POST':
        form = BookingForm(request.POST, instance=Booking())

        if form.is_valid():
            #user = request.user
            student_tickets = form.cleaned_data.get('student_tickets')
            child_tickets = form.cleaned_data.get('child_tickets')
            adult_tickets = form.cleaned_data.get('adult_tickets')
            if showing.booking_is_valid(student_tickets,child_tickets,adult_tickets):
                user_id = int(request.session['id'])
                user = User.objects.get(id=user_id)
                balance = user.balance
                print("your balance",balance)
                total_price = (student_tickets * student_ticket_price )+ (child_tickets * child_ticket_price)+ (adult_tickets *adult_ticket_price)
                print("total price ",total_price)
                new_balance = balance - total_price
                if new_balance > -150:
                    booking = Booking(showing=showing, student_tickets=student_tickets, child_tickets=child_tickets, adult_tickets=adult_tickets,user=user) 
                    booking.save()
                    user.balance = new_balance
                    user.save()
                else:
                    forms = BookingForm()
                    messages.error(request,"Insufficient Funds! Please top up your account!")
                    return render(request, 'cinema/booking_film.html', {'showing': showing, 'form': forms})
            else:
                messages.error(request,"There aren't that many seats availible sorry!")
                return render(request, 'cinema/booking_film.html', {'showing': showing, 'form': form})
            return redirect('cinema:list_films')
        else:
            forms = BookingForm()
            return render(request, 'cinema/booking_film.html', {'showing': showing, 'form': forms})
    else:
        form = BookingForm()
        return render(request, 'cinema/booking_film.html', {'showing': showing, 'form': form})
    #return render(request,'customer/booking.html', {'form': form })

# club rep paying directly
def book_showing_cr(request, showing_id, user_required = True , user_types_required=(User.UserType.CLUBREP)):
    showing = CinemaManager.get_showing(showing_id)
    # for key,value in request.session.items():
    #     print ('{} =>{}'.format(key,value))
    if request.method == 'POST':
        forms = BookingForm_cr(request.POST, instance=Booking())
        

        if forms.is_valid():
            
            cr_tickets = forms.cleaned_data.get('cr_tickets')
            if showing.booking_is_valid(cr_tickets=cr_tickets):
                user_id = int(request.session['id'])
                user = User.objects.get(id=user_id)
                balance = user.balance
                print("your balance",balance)
                total_price = (cr_tickets * cr_ticket_price)
                print("total price ",total_price)
                new_balance = balance - total_price
                if new_balance > -150:
                    booking = Booking(showing=showing, cr_tickets = cr_tickets,user=user) 
                    booking.save()
                    user.balance = new_balance
                    user.save()
                    print("balance ",user.balance)
                else:
                    forms = BookingForm_cr()
                    messages.error(request,"Insufficient Funds! Please top up your account!")
                    return render(request, 'cinema/booking_film.html', {'showing': showing, 'form': forms})
            else:
                forms = BookingForm_cr()
                messages.error(request,"There aren't that many seats availible sorry!")
                return render(request, 'cinema/booking_film.html', {'showing': showing, 'form': forms})
            return redirect('cinema:list_films')
        else:
            forms = BookingForm_cr()
            return render(request, 'cinema/booking_film.html', {'showing': showing, 'form': forms})
    else:
        forms = BookingForm_cr()
        return render(request, 'cinema/booking_film.html', {'showing': showing, 'form': forms})



def settling_balance(request, showing_id, user_required = True , user_types_required=(User.UserType.STUDENT,User.UserType.CLUBREP)):
    #showing = CinemaManager.get_showing(showing_id)
    
    if request.method == 'POST':
        request.session['version']= 3
        return redirect('customer:checkout')

# booking for guest
def book_showing_guest(request, showing_id):
    showing = CinemaManager.get_showing(showing_id)


    if request.method == 'POST':
        form = BookingForm_g(request.POST, instance=Booking())
        if form.is_valid():
            #user = request.user
            
            adult_tickets = form.cleaned_data.get('adult_tickets')
            child_tickets = form.cleaned_data.get('child_tickets')
            request.session['child']= child_tickets
            # total_price = calculate_total_price(showing, student_tickets, child_tickets, adult_tickets)
            if showing.booking_is_valid(adult_tickets=adult_tickets,child_tickets=child_tickets):
                request.session['version']= 4
                request.session['adult']= adult_tickets
                request.session['showing_info'] = showing_id 

                return redirect('customer:checkout')
            else:
                forms = BookingForm_g()
                messages.error(request,"Form invalid")
                return render(request, 'cinema/booking_film.html', {'showing': showing, 'form': forms})
        else:
            forms = BookingForm_g()
            return render(request, 'cinema/booking_film.html', {'showing': showing, 'form': forms})
    else:
        form = BookingForm_g()
        return render(request, 'cinema/booking_film.html', {'showing': showing, 'form': form})

# booking for AM CM
def book_showing_AM_CM(request, showing_id, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER,User.UserType.ACCOUNTSMANAGER)):
    showing = CinemaManager.get_showing(showing_id)


    if request.method == 'POST':
        form = BookingForm_g(request.POST, instance=Booking())
        if form.is_valid():
            #user = request.user
            
            adult_tickets = form.cleaned_data.get('adult_tickets')
            child_tickets = form.cleaned_data.get('child_tickets')
            if showing.booking_is_valid(adult_tickets=adult_tickets,child_tickets=child_tickets):
                request.session['child']= child_tickets
                # total_price = calculate_total_price(showing, student_tickets, child_tickets, adult_tickets)

                request.session['version']= 5
                request.session['adult']= adult_tickets
                request.session['showing_info'] = showing_id 

                return redirect('customer:checkout')
            else:
                forms = BookingForm_g()
                messages.error(request,"There aren't that many seats sorry")
                return render(request, 'cinema/booking_film.html', {'showing': showing, 'form': forms})

        else:
            forms = BookingForm_g()
            return render(request, 'cinema/booking_film.html', {'showing': showing, 'form': forms})
    else:
        form = BookingForm_g()
        return render(request, 'cinema/booking_film.html', {'showing': showing, 'form': form})



#Function to pull data on the most popular films from api
def movie_api_request(page):
    url = "https://moviesdatabase.p.rapidapi.com/titles"

    querystring = {"titleType":"movie","list":"top_boxoffice_200","page":f"{page}"}

    headers = {
        "X-RapidAPI-Key": "6dff3c3b88msh55e37c0281bc11fp17a0f4jsn7400839f9a93",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    try:
        resp_dict = response.json()
    except JSONDecodeError: 
        print("error")

    df = pd.DataFrame(resp_dict.get("results"))
    data = []
    for x in range(0,9):
        data.append({"title":df["titleText"][x]["text"],"image":df["primaryImage"][x]["url"]})
    return data
