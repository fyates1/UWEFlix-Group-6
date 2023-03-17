from django import forms
from .models import Club
from django.forms import ModelForm


class clubRegister(ModelForm):
    #First_Name = forms.CharField(max_length=50)
    #Last_Name = forms.CharField(max_length=1)
    #club= forms.CharField(max_length=50)
    class Meta:
        model = Club
        fields = ('clubName', 'memberCount','discount', 'streetNo', 'street','city', 'postcode','landlineNo', 'mobileNo', 'email')
        labels = {
            'clubName': 'Club Name',
            'memberCount': 'Members',
            'discount': 'Discount',
            'streetNo': 'Street Number',
            'street': 'Street',
            'city': 'City',
            'postcode': 'Post Code',
            'landlineNo': 'Landline Number',
            'mobileNo': 'Mobile Number',
            'email': 'Email',
        }
    # def save(self, commit=True):
    #     user = super(RegisterFrom, self).save(commit=False)
    #     user.club = self.cleaned_data["club"]
    #     if commit:
    #         user.save()
    #     return user