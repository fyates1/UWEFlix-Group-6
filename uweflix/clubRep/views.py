
from django.shortcuts import render, redirect, get_object_or_404, reverse
import re

from django.http import HttpResponse, HttpResponseRedirect
from .models import Club
from accounts.models import Transaction
from .forms import clubRegister, settle_accounts
from accounts.models import User
import requests
from django.contrib import messages

# can be used to authenticate users
# from django.contrib.auth.decorators import login_required


# Create your views here.

def view_transactions(request):
    club = request.user.club
    transactions = Transaction.objects.filter(club=club)
    return render(request, 'clubRep/view_transactions.html', {'transactions': transactions})


def addClub(response,user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
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
            return redirect(reverse('clubRep:view') + '?message=Club successfully created!')
    else:
        form = clubRegister()

        if 'submitted' in response.GET:
            submitted = True
        return render(response, "clubRep/registerClub.html", {'form':form, 'submitted':submitted})

def view_clubs(request, user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    #message = request.GET.get('message') # Get any message from previous pages
    clubs_view = Club.objects.all()
    return render(request, "clubRep/view.html", {"clubs_view":clubs_view, "message":message})

def view_club(response, club_id,user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    club= Club.objects.get(pk=club_id)

    return render(response,"clubRep/view_club.html", {"club":club} )


def settle(request,user_required = True , user_types_required=(User.UserType.CLUBREP,User.UserType.STUDENT)):
    #club = Club.objects.first()
    user_id = int(request.session['id'])
    user = User.objects.get(id=user_id)

    request.session['version']= 3
    if request.method == 'POST':
        form = settle_accounts(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('clubRep:settle')
    else:
        form = settle_accounts(instance=user)
        #request.session['version']= 3
        #return redirect('customer:checkout')
    # Get transaction history for the club
    #transactions = Transaction.objects.filter(user=user)

    return render(request, 'clubRep/settle.html', {'form': form,}) #'transactions': transactions})

# def settling_balance(request, showing_id):
#     #showing = CinemaManager.get_showing(showing_id)
    
#     if request.method == 'POST':
#         request.session['version']= 3
#         return redirect('customer:checkout')


def delete_club(response, club_id,user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    club = Club.objects.get(pk=club_id)
    club.delete()
    return redirect(reverse('clubRep:view') + f'?message=The club {club} was deleted successfully!')

def update_club(request, club_id,user_required = True , user_types_required=(User.UserType.CINEMAMANAGER)):
    club = Club.objects.get(pk=club_id)
    form = clubRegister(request.POST or None,instance=club)
    if form.is_valid():
            form.save()
            return redirect(reverse('clubRep:view') + f'?message=The club {club} was updated successfully!')
    return render(request,"clubRep/update_club.html",{"club":club, "form":form})
