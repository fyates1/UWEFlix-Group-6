from django import forms
from django.forms import ModelForm
from .models import screen,row,seat,film,showing
from django.contrib.admin.widgets import AdminSplitDateTime,AdminDateWidget,AdminTimeWidget

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
class FilmForm(ModelForm):
    class Meta:
        model = film
        fields = "__all__"
class ShowingForm(ModelForm):
   
    class Meta:
        model = showing
        fields = ("date","startTime","film","screen")

class BookingForm(ModelForm):
    class Meta:
        #model = booking
        fields = "__all__"
    