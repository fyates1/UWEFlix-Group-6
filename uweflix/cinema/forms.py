from django import forms
from django.forms import ModelForm
from .models import screen,row,seat,film,showing,Booking
from django.contrib.admin.widgets import AdminSplitDateTime,AdminDateWidget,AdminTimeWidget
from django.core.exceptions import ValidationError
from django.utils import timezone


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
        model = Booking
        fields = ("student_tickets","child_tickets","adult_tickets")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        student_tickets = self.cleaned_data['student_tickets']
        child_tickets = self.cleaned_data['child_tickets']
        adult_tickets = self.cleaned_data['adult_tickets']
        instance.user = current_user
        instance.student_tickets = student_tickets
        instance.child_tickets = child_tickets
        instance.adult_tickets = adult_tickets
        # instance.total_price = calculate_total_price(instance.showing, student_tickets, child_tickets, adult_tickets)
        if commit:
            instance.save()
        return instance

class BookingForm_cr(ModelForm):
    
    class Meta:
        model = Booking
        fields = ("cr_tickets",)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        cr_tickets = self.cleaned_data["cr_tickets"]

        instance.cr_tickets = cr_tickets

        # instance.total_price = calculate_total_price(instance.showing, student_tickets, child_tickets, adult_tickets)
        if commit:
            instance.save()
        return instance


# class BookingForm_cr(ModelForm):
   
#     class Meta:
#         model = Booking
#         fields = ("cr_tickets", "showing")