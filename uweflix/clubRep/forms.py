from django import forms
from .models import Club
from django.forms import ModelForm

DISCOUNT_RATE = [('15', '15')]



class clubRegister(ModelForm):

    class Meta:
        model = Club
        fields = ('clubName', 'memberCount', 'email','landlineNo', 'mobileNo','discount', 'streetNo', 'street','city', 'postcode')
        labels = {
            'clubName': 'Club Name',
            'memberCount': 'Members',
            'email': 'Email',
            'landlineNo': 'Landline Number',
            'mobileNo': 'Mobile Number',
            'discount': 'Discount',
            'streetNo': 'Street Number',
            'street': 'Street',
            'city': 'City',
            'postcode': 'Post Code',
        }
        widgets = {

            'discount':forms.Select(choices=DISCOUNT_RATE,attrs={'class':'form-control','placeholder':'Discount Rate'}),
        }
