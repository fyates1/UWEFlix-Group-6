from django import forms
from django.forms import ModelForm
from .models import screen,row,seat

#Screen Forms
class ScreenForm(ModelForm):
    class Meta:
        model = screen
        fields = "__all__"

class RowForm(ModelForm):
    class Meta:
        model = row
        fields = "__all__"

class SeatForm(ModelForm):
    class Meta:
        model = seat
        fields = "__all__"
