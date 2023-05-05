from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext_lazy as _
from django.db import models
from django import forms
from django.db.models.signals import pre_save
from django.dispatch import receiver
from clubRep.models import Club
from accounts.validation import *
from django.core.validators import MinValueValidator, MaxValueValidator


# ----------------- Models -----------------
#region
# Stores the payment information
class PaymentDetails(models.Model):
    # Payment Information
    cardNumber = models.CharField(max_length=16, validators=[validateCardNumber])
    expirationDate = models.CharField(max_length=5, validators=[validateExpirationDate])
    cvv = models.CharField(max_length=4, validators=[validate_cvv])
    cardHolderName = models.CharField(max_length=255, validators=[validate_cardholder_name])

class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentDetails
        fields = '__all__'

# Stores information about individually registered users and their account details
class User(models.Model):
    # Identifiers
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    # User Type
    class UserType(models.TextChoices):
        CUSTOMER = 'C', _('Customer')
        STUDENT = 'S', _('Student')
        CLUBREP = 'CR', _('Club Rep')
        ACCOUNTSMANAGER = 'AM', _('Accounts Manager')
        CINEMAMANAGER = 'CM', _('Cinema Manager')
        # SUPERUSER = 'SU', _('Super User')

    userType = models.CharField(
        max_length = 2,
        choices = UserType.choices,
        default = UserType.CUSTOMER
    )

    # Personal Info
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    dateOfBirth = models.DateField()
    userEmail = models.CharField(max_length=255)

    # Affiliated Club
    affiliatedClub = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True)

    # Payment information
    paymentDetails = models.ForeignKey(PaymentDetails, on_delete=models.CASCADE, blank=True, null=True)
    balance = models.IntegerField(default=0, validators=[MinValueValidator(-150)])

    # def encryptPassword(self, plainPassword):
    #     self.password = make_password(plainPassword)

    # def checkPassword(self, plainPassword):
    #     if check_password(plainPassword, self.password):
    #         return True
    #     else:
    #         return False
    # def checkPassword(self, plainPassword):
    #     return check_password(plainPassword, self.password)


    def getUserType(self):
        return self.userType

    def __str__(self):
        return f"{self.username} ({self.firstName} {self.lastName})"

class UserForm(forms.ModelForm):
    # Form for User model
    class Meta:
        model = User
        fields = ('username', 'password', 'userType', 'firstName', 'lastName', 'dateOfBirth', 'userEmail', 'affiliatedClub', 'paymentDetails',) #'__all__'
        widgets = {
            'dateOfBirth': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                    'placeholder': 'Select a date',
                    'type': 'date'
                }),
            'password': forms.TextInput(
                attrs={
                    'placeholder': 'Enter a password',
                    'type': 'password'
                }
            )
        }

class RegisterForm(forms.ModelForm):
    # Form for User model
    class Meta:
        model = User
        fields = ('username', 'password', 'userType', 'firstName', 'lastName', 'dateOfBirth', 'userEmail', 'affiliatedClub', 'paymentDetails',) #'__all__'
        widgets = {
            'dateOfBirth': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                    'placeholder': 'Select a date',
                    'type': 'date'
                }),
            'password': forms.TextInput(
                attrs={
                    'placeholder': 'Enter a password',
                    'type': 'password'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['userType'].choices = [('C', 'Customer'), ('S', 'Student')]

class Transaction(models.Model):
    #club = models.ForeignKey(Club, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
#endregion

# ----------------- Receivers -----------------
#region
# This should run whenever the User model wishes to save itself
# @receiver(pre_save, sender=User)
# def encrypt_user_password(sender, instance, **kwargs):
#     # Checks if password field is not None
#     if instance.password:
#         # Runs encryptPassword before .save() is completed
#         instance.encryptPassword(instance.password)
#endregion