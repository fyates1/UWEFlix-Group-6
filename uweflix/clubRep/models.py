# from django.db import models
# from django.core.exceptions import ValidationError
# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from validate_email import validate_email
# from phonenumber_field.formfields import PhoneNumberField

from django.utils.translation import gettext_lazy as _
from django.db import models


import uuid, re, datetime
from datetime import date, timedelta
from accounts.validation import *

# Create your models here.

class Club(models.Model):
    # Identifiers
    clubName = models.CharField(max_length=255)
    memberCount = models.IntegerField(default=1)
    email = models.CharField(max_length=20)
    landlineNo = models.IntegerField(null=True)# validators=[isLandlineNumber], null=True)
    mobileNo = models.IntegerField(null=True)# validators=[isMobileNumber], null=True)
    discount = models.IntegerField(default=2)

    # Location Details
    streetNo = models.IntegerField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)

    #added balance for the club reps to use
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.clubName
    
# class Transaction(models.Model):
#     #club = models.ForeignKey(Club, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now_add=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.CharField(max_length=255)


# class ClubForm(forms.ModelForm):
#     # Form for Club model
#     class Meta:
#         model = Club
#         fields = '__all__'