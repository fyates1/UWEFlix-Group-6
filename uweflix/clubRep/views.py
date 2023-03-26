
from django.shortcuts import render, redirect, get_object_or_404
import re

from django.http import HttpResponse, HttpResponseRedirect
from .models import Club
from .forms import clubRegister 


# Create your views here.

def addClub(response):
    #response.user
    submitted = False
    if response.method == "POST":
        form = clubRegister(response.POST)
        if form.is_valid():
            #n= form.cleaned_data["name"]
            #t = Club(name=n)
            #t.save() 
            form.save()
            #response.user.clubname.add(t)
            return redirect('clubRep:view')
    else:
        form = clubRegister()

        if 'submitted' in response.GET:
            submitted = True
        return render(response, "clubRep/registerClub.html", {'form':form, 'submitted':submitted})

def view_clubs(response):
    clubs_view = Club.objects.all()
    return render(response, "clubRep/view.html", {"clubs_view":clubs_view})

def view_club(response, club_id):
    club= Club.objects.get(pk=club_id)

    return render(response,"clubRep/view_club.html", {"club":club} )


def delete_club(response, club_id):
    club = Club.objects.get(pk=club_id)
    club.delete()
    return redirect('clubRep:view')