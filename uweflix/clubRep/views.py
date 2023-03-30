
from django.shortcuts import render, redirect, get_object_or_404, reverse
import re

from django.http import HttpResponse, HttpResponseRedirect
from .models import Club, Transaction
from .forms import clubRegister, settle_accounts

# can be used to authenticate users
# from django.contrib.auth.decorators import login_required


# Create your views here.

def view_transactions(request):
    club = request.user.club
    transactions = Transaction.objects.filter(club=club)
    return render(request, 'clubRep/view_transactions.html', {'transactions': transactions})


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


def settle(request):
    club = Club.objects.first()
    if request.method == 'POST':
        form = settle_accounts(request.POST, instance=club)
        if form.is_valid():
            form.save()
            return redirect('clubRep:settle')
    else:
        form = settle_accounts(instance=club)
        
    # Get transaction history for the club
    transactions = Transaction.objects.filter(club=club)

    return render(request, 'clubRep/settle.html', {'form': form, 'transactions': transactions})

def delete_club(response, club_id):
    club = Club.objects.get(pk=club_id)
    club.delete()
    return redirect('clubRep:view')