from django.template import loader
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *

# Index for the accounts management subsection
def index(request):
    # This is the main page of the accounts manager
    # TODO this needs to be changed as this is mainly to server as a debugging tool to perform quick tests
    # TODO This will need to be segmented into seperate sites that are only accessable to those with perms
    userList = User.objects.all()
    clubList = Club.objects.all()
    repList = Representitive.objects.all()
    message = request.GET.get('message')

    context = {
        'userList': userList,
        'clubList': clubList,
        'repList': repList,
        'message': message
    }

    return render(request, 'accounts/index.html', context)

def manageUser(request, userID):
    user = get_object_or_404(User, pk=userID)
    userForm = UserForm(request.POST or None, instance=user)

    context = {
        'user': user,
        'userForm': userForm
    }

    # When used to render page
    if request.method != 'POST':
        return render(request, 'accounts/manageUser.html', context)

    if request.POST.get('submit', False):# If the update button is pressed
        if userForm.is_valid():
            user.encryptPassword(userForm.cleaned_data['password'])
            userForm.save()
            return redirect(reverse('accounts:index') + '?message=Update Successful')

        else:
            return render(request, 'accounts/manageUser.html', context)

    elif request.POST.get('delete', False): # If the delete button is pressed
        user.delete()
        return redirect(reverse('accounts:index') + '?message=Entry Deleted')

def createUser(request):
    userForm = UserForm(request.POST or None)

    context = {
        "userForm": userForm
    }

    if request.method != 'POST':
        return render(request, 'accounts/createUser.html', context)

    if userForm.is_valid():
        user = userForm.save(commit=False)
        user.encryptPassword(userForm.cleaned_data['password'])
        user.save()
        return redirect(reverse('accounts:index') + '?message=New User Created')
    else:
        return render(request, 'accounts/createUser.html', context)

def manageClub(request, clubID):
    club = get_object_or_404(Club, id = clubID)
    clubForm = ClubForm(request.POST or None, instance=club)

    context = {
        "club": club,
        'clubForm': clubForm
    }

    # If form is yet to be filled
    if request.method != 'POST':
        return render(request, 'accounts/manageClub.html', context)

    # If form has returned with inputs
    if request.POST.get('submit', False): # If the update button is pressed
        if clubForm.is_valid():
            clubForm.save()
            return redirect(reverse('accounts:index') + '?message=Update Successful')
        else:
            return render(request, 'accounts/manageClub.html', context)
    elif request.POST.get('delete', False): # If the delete button is pressed
        club.delete()
        return redirect(reverse('accounts:index') + '?message=Entry Deleted')

def createClub(request):
    clubForm = ClubForm(request.POST or None)

    context = {
        "clubForm": clubForm
    }

    if request.method != 'POST':
        return render(request, 'accounts/createClub.html', context)

    # When the form returns with an input
    clubForm = ClubForm(request.POST)

    if clubForm.is_valid():
        clubForm.save()
        return redirect(reverse('accounts:index') + '?message=New User Created')
    else:
        return render(request, 'accounts/createClub.html', context)

def createRep(request):
    repForm = RepForm(request.POST or None)

    context = {
        "repForm": repForm
    }

    if request.method != 'POST':
        return render(request, 'accounts/createRep.html', context)

    if repForm.is_valid():
        rep = repForm.save(commit=False)
        rep.encryptPassword(repForm.cleaned_data['password'])
        repForm.save()
        return redirect(reverse('accounts:index') + '?message=New Representitive Assigned')
    else:
        return render(request, 'accounts/createRep.html', context)

def manageRep(request, repID):
    rep = get_object_or_404(Representitive, id=repID)
    repForm = RepForm(request.POST or None, instance=rep)

    context = {
        'rep': rep,
        'repForm': repForm
    }

    # If form is yet to be filled
    if request.method != 'POST':
        return render(request, 'accounts/manageRep.html', context)

    # If form has returned with inputs
    if request.POST.get('submit', False): # If the update button is pressed
        if repForm.is_valid():
            rep.encryptPassword(repForm.cleaned_data['password'])
            repForm.save()
            return redirect(reverse('accounts:index') + '?message=Update Successful')
        else:
            return render(request, 'accounts/manageClub.html', context)
    elif request.POST.get('delete', False): # If the delete button is pressed
        rep.delete()
        return redirect(reverse('accounts:index') + '?message=Entry Deleted')

def selectStatement(request):
    # userPayments = UserPurchaseHistory.objects.all()
    # clubPayments = ClubPurchaseHistory.objects.all()
    userList = User.objects.all()
    clubList = Club.objects.all()

    context = {
        # 'userPayment': userPayments,
        # 'clubPayments': clubPayments,
        'userList': userList,
        'clubList': clubList
    }

    return render(request, 'accounts/selectStatements.html', context)

def seeUserStatement(request, userID):
    history = UserPurchaseHistory.objects.filter(user__id=userID)
    name = history[0].user.firstName + " " + history[0].user.lastName
    total = {
        'spent': 0,
        'bought': 0
    }

    for statement in history:
        total['spent'] += statement.totalCost
        total['bought'] += statement.quantity

    context = {
        'history': history,
        'total': total,
        'name': name
    }

    return render(request, 'accounts/seeStatement.html', context)

def seeClubStatment(request, clubID):
    history = ClubPurchaseHistory.objects.filter(club__id=clubID)
    name = "the " + history[0].club.clubName + " Club"
    total = {
        'spent': 0,
        'bought': 0
    }

    for statement in history:
        total['spent'] += statement.totalCost
        total['bought'] += statement.quantity

    context = {
        'history': history,
        'total': total,
        'name': name
    }

    return render(request, 'accounts/seeStatement.html', context)

# This is where all the accounts management stuff will be on one page
def manageAccounts(request, userID):
    userList = User.objects.all()
    message = request.GET.get('message')

    if userID != 0:
        user = User.objects.get(id=userID)
        userForm = UserForm(request.POST or None, instance=user)
    else:
        # This will be none when no account is selected because the form wont even be visible at that time
        user = None
        userForm = None # TODO Check if this can be called like a form without erroring OTHERWISE this will get a blank form

    context = {
        'userList': userList,
        'user': user,
        'userForm': userForm,
        'message': message
    }

    # TODO Process the inputted shit from the form whether it is an update or delete

    if request.method != 'POST':
        return render(request, 'accounts/allAccounts.html', context)

    if request.POST.get('delete', False): # If the delete button is pressed
        user.delete()
        return redirect(reverse('accounts:manageAccounts', kwargs={'userID': userID}) + '?message=Entry Deleted')

    elif request.POST.get('submit', False): # If the submit button is pressed
        if userForm.is_valid():
            user.encryptPassword(userForm.cleaned_data['password'])
            userForm.save()
            return redirect(reverse('accounts:manageAccounts', kwargs={'userID': userID}) + '?message=Update Successful')

        else:
            return render(request, 'accounts/manageUser.html', context)

# def manageSelectedAccounts(request, userID):
#     userList = User.objects.all()

#     if userID != 0:
#         user = User.objects.get(id=userID)
#         userForm = UserForm(request.POST or None, instance=user)
#     else:
#         # This will be none when no account is selected because the form wont even be visible at that time
#         user = None
#         userForm = None # TODO Check if this can be called like a form without erroring OTHERWISE this will get a blank form

#     context = {
#         'userList': userList,
#         'user': user,
#         'userForm': userForm
#     }

#     # TODO Process the inputted shit from the form whether it is an update or delete

#     return render(request, 'accounts/allAccounts.html', context)
