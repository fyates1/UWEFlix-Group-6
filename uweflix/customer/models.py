import django 
from django.db import models
from datetime import datetime, date,timezone
from django.utils import timezone
# Create your models here.
from cinema.models import *

class TicketBooking(models.Model):
    
    ticket_date = models.DateField(default=django.utils.timezone.now)
    ticket_count = models.IntegerField(blank=False)
    TICKET_CHOICES = (
        ('Student', 'Student'),
        ('Child', 'Child'),
        ('Adult', 'Adult'),
    )
    ticket_type = models.CharField(choices=TICKET_CHOICES, max_length=15)
    showing = models.ForeignKey(showing, on_delete=models.CASCADE)
    # buyer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # credit_card_info = models.CharField(max_length=30)
    # credit_card_name = models.CharField(max_length=30)
    # credit_card_exp = models.CharField(max_length=30)
    # status = models.CharField(max_length=30)

    def __str__(self):
        return "{0} - {1}  ".format(self.showing)



class Basket(models.Model):



    def __str__(self):
        return 