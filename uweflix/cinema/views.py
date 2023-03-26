from django.shortcuts import render,redirect
from .forms import ScreenForm,RowForm,SeatForm,FilmForm,ShowingForm
from .models import screen,row,film,showing
from django.http import HttpResponseRedirect
from customer.forms import BookingForm

class CinemaManager():
    def get_screenList():
        List = screen.objects.all()
        return List
    def get_screen(id):
        return screen.objects.get(pk=id)
    def get_rowList():
        List = row.objects.all()
        return List
    def get_row(id):
        return row.objects.get(pk=id)
    def get_film(id):
        return film.objects.get(pk=id)

    def add_screen(request):
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

    def add_row(request):
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

    def add_seat(request):
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

    def add_film(request):
        submitted = False
        if request.method == "POST":
            form = FilmForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/cinema/add_film?submitted=True")
        else:
            form = FilmForm
            if "submitted" in request.GET:
                submitted = True
        return render(request,"cinema/add_film.html",{"form":form ,"submitted":submitted})

def add_screen(request):
    return CinemaManager.add_screen(request)

def add_row(request):
    return CinemaManager.add_row(request)

def list_screens(request):
    screen_list = CinemaManager.get_screenList()
    return render(request,"cinema/screens.html",{"screen_list":screen_list,})

def list_rows(request):
    row_list = row.objects.all()
    return render(request,"cinema/rows.html",{"row_list":row_list,})

def show_screen(request,screen_id):
    Screen = CinemaManager.get_screen(screen_id)
    return render(request,"cinema/show_screen.html",{"screen":Screen})

def show_row(request,row_id):
    Row = CinemaManager.get_row(row_id)
    return render(request,"cinema/show_row.html",{"row":Row})

def update_screen(request, screen_id):
    Screen = CinemaManager.get_screen(screen_id)
    form = ScreenForm(request.POST or None,instance=Screen)
    if form.is_valid():
            form.save()
            return redirect('list_screens')
    return render(request,"cinema/update_screen.html",{"screen":Screen, "form":form})

def update_row(request, row_id):
    Row = CinemaManager.get_row(row_id)
    form = RowForm(request.POST or None,instance=Row)
    if form.is_valid():
            form.save()
            return redirect('list_rows')
    return render(request,"cinema/update_row.html",{"row":Row, "form":form})

def delete_screen(request,screen_id):
    Screen = CinemaManager.get_screen(screen_id)
    Screen.delete()
    return redirect("list_screens")
    
def delete_row(request,row_id):
    Row = CinemaManager.get_row(row_id)
    Row.delete()
    return redirect("list_rows")

def add_seat(request):
    return CinemaManager.add_seat(request)

def add_film(request):
    return CinemaManager.add_film(request)

def list_films(request):
    film_listing = film.objects.all()
    return render(request,"cinema/films.html",{"film_listing":film_listing})

def show_film(request,film_id):
    film = CinemaManager.get_film(film_id)
    return render(request,"cinema/show_film.html",{"film":film})

def update_film(request, film_id):
    Film = CinemaManager.get_film(film_id)
    form = FilmForm(request.POST or None,instance=Film)
    if form.is_valid():
            form.save()
            return redirect('list_films')
    return render(request,"cinema/update_film.html",{"film":Film, "form":form})

def delete_film(request,film_id):
    Film = CinemaManager.get_film(film_id)
    Film.delete()
    return redirect("cinema:list_films")

def add_showing(request):
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
def list_showings(request):
    showing_list = showing.objects.all()
    return render(request,"cinema/showings.html",{"showing_list":showing_list})

# Not used currently. Although keep
def index(request):
    index = film.objects.all()
    return render(request,"cinema/index.html",{"index":index})

# Main display screen
def display_films(request):
    film_list = film.objects.all()
    return render(request,"cinema/display_films.html",{"film_list":film_list})

# Film details when clicking
def film_showing(request, _id):
    film_showings = film.objects.get(id=_id)
    return render(request,"cinema/film_showing.html",{"film_showings":film_showings})

# Booking 
def booking_sheet(request):
    form = BookingForm()
    return render(request,'customer/booking.html', {'form': form })