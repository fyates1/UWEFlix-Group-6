from django import forms
from .models import Club
from django.forms import ModelForm
from accounts.models import User
from accounts.models import Transaction
import requests
from django.contrib import messages

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


class settle_accounts(forms.ModelForm):
    # user_id = int(request.session['id'])
    # user = User.objects.get(id=user_id)
    # balance = user.balance
    #current_balance = forms.IntegerField(disabled=True)

    class Meta:
        model = User
        fields = ('balance',)
 
        
        widgets = {
            'balance': forms.TextInput(attrs={'readonly': True}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['balance'].initial = self.instance.balance

    # def clean_balance(self):
    #     balance = self.cleaned_data['balance']
    #     return balance

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     balance = self.cleaned_data['balance']
    #     amount = self.cleaned_data['balance'] + self.cleaned_data['current_balance']
    #     if amount == 0:
    #         description = 'Settled Accounts'
    #     elif balance > 0:
    #         description = f'Added {balance} to balance'
    #     else:
    #         description = f'Deducted {-balance} from balance'
    #     Transaction.objects.create(club=instance, amount=amount, description=description)
    #     instance.balance = amount
    #     if commit:
    #         instance.save()
    #     return instance