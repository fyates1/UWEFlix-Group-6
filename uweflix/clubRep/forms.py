from django import forms
from .models import Club
from django.forms import ModelForm

DISCOUNT_RATE = [('15', '15')]



class clubRegister(ModelForm):
    #First_Name = forms.CharField(max_length=50)
    #Last_Name = forms.CharField(max_length=1)
    #club= forms.CharField(max_length=50)
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
    # def save(self, commit=True):
    #     user = super(RegisterFrom, self).save(commit=False)
    #     user.club = self.cleaned_data["club"]
    #     if commit:
    #         user.save()
    #     return user