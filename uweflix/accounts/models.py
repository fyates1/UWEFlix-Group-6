from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext_lazy as _
from django.db import models
from django import forms
import uuid, re, datetime
from datetime import date, timedelta
from django.db.models.signals import pre_save
from django.dispatch import receiver

# ----------------- Validators -----------------
#region

# Check validity of mobile number
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

# Algorithm to check the validation of a card number
def luhn_check(card_number):
    """Validate card number using the Luhn algorithm"""
    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10 == 0

# Checks the validity of card number
def validateCardNumber(value):
    cardNumber = re.sub("[^0-9]", "", value)
    if not re.match(r"^[0-9]{16}$", cardNumber):
        raise forms.ValidationError("Invalid card number")
    if not luhn_check(cardNumber):
        raise forms.ValidationError("Invalid card number")

# Checks the validity of the expiration date
def validateExpirationDate(value):
    if not re.match(r"^(0[1-9]|1[0-2])\/[0-9]{2}$", value):
        raise forms.ValidationError("Invalid expiration date (Must be MM/YY)")
    month, year = value.split("/")
    if int(year) < datetime.datetime.now().year % 100:
        raise forms.ValidationError("Invalid expiration date (Must be MM/YY)")
    if int(year) == datetime.datetime.now().year % 100 and int(month) < datetime.datetime.now().month:
        raise forms.ValidationError("Invalid expiration date (Must be MM/YY)")

# Checks the validity of cvv
def validate_cvv(value):
    if not re.match(r"^[0-9]{3,4}$", value):
        raise forms.ValidationError("Invalid CVV/CVC code")

# Checks the validity of card name
def validate_cardholder_name(value):
    if not value.strip():
        raise forms.ValidationError("Invalid cardholder name")
#endregion

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
        # CUSTOMER = 'G', _('Guest')
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

    # Affiliated Club
    # TODO - Make this work when Haroun/Lewis finish their model
    # affiliatedClub = models.ForeignKey(Club, on_delete=models.CASCADE)

    # Payment information
    paymentDetails = models.ForeignKey(PaymentDetails, on_delete=models.CASCADE, blank=True, null=True)

    def encryptPassword(self, plainPassword):
        self.password = make_password(plainPassword)

    def checkPassword(self, plainPassword):
        if check_password(plainPassword, self.password):
            return True
        else:
            return False
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
        fields = '__all__'
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
#endregion

# ----------------- Receivers -----------------
#region
# This should run whenever the User model wishes to save itself
@receiver(pre_save, sender=User)
def encrypt_user_password(sender, instance, **kwargs):
    # Checks if password field is not None
    if instance.password:
        # Runs encryptPassword before .save() is completed
        instance.encryptPassword(instance.password)
#endregion