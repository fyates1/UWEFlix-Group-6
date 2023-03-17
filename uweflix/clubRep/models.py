# from django.db import models
# from django.core.exceptions import ValidationError
# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from validate_email import validate_email
# from phonenumber_field.formfields import PhoneNumberField

from django.utils.translation import gettext_lazy as _
from django.db import models
from django import forms
import uuid, re, datetime
from datetime import date, timedelta
# Create your models here.

# Used to store information about clubs
def isMobileNumber(value):
    # This is mainly for UK numbers just to simplify things but later on i might want to make this work for more numbers
    mobileRegex = re.compile(r'^\d{11}$')

    if not mobileRegex.match(value):
        raise forms.ValidationError("Invalid Mobile Number (Make sure it's a UK number)")

# Check validity of landline number
def isLandlineNumber(value):
    # Once again this is mainly for UK numbers
    landlineRegex = re.compile(r'^\d{5}\d{6}$')

    if not landlineRegex.match(value):
        raise forms.ValidationError("Invalid Landline Number (Make sure it's a UK number)")

class Club(models.Model):
    # Identifiers
    clubName = models.CharField(max_length=255)
    memberCount = models.IntegerField(default=1)
    email = models.CharField(max_length=20)
    landlineNo = models.CharField(max_length=255, validators=[isLandlineNumber], null=True)
    mobileNo = models.CharField(max_length=20, validators=[isMobileNumber], null=True)

    discount = models.IntegerField(default=2)

    # Location Details
    streetNo = models.IntegerField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)

    # Contact Details

    def __str__(self):
        return self.clubName

# class ClubForm(forms.ModelForm):
#     # Form for Club model
#     class Meta:
#         model = Club
#         fields = '__all__'