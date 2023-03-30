import re, datetime
from django import forms

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
