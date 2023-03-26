from django import forms
from django.forms import ModelForm
from .models import TicketBooking
from cinema.models import showing
from django.contrib.admin.widgets import AdminSplitDateTime,AdminDateWidget,AdminTimeWidget


class BookingForm(ModelForm):
    class Meta:
        model = TicketBooking
        fields = "__all__"
    