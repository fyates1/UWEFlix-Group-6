from django.shortcuts import render,redirect
from .forms import ScreenForm,RowForm,SeatForm
from .models import screen,row
from django.http import HttpResponseRedirect
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