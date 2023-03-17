from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
import re
from django.utils.timezone import datetime
from django.http import HttpResponse, HttpResponseRedirect
from .models import Club#, MyModel
from .forms import clubRegister #, MyModelForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView

# Create your views here.

def addClub(response):
    #response.user
    submitted = False
    if response.method == "POST":
        form = clubRegister(response.POST)
        if form.is_valid():
            n= form.cleaned_data["name"]
            #t = Club(name=n)
            #t.save() 
            form.save()
            #response.user.clubname.add(t)
        return HttpResponseRedirect("/superuser")
    else:
        form = clubRegister()
    return render(response, "clubRep/registerClub.html", {"form":form, 'submitted':submitted})