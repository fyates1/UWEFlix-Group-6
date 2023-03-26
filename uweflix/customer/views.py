

from django.shortcuts import render, redirect, get_object_or_404
import re

from django.http import HttpResponse, HttpResponseRedirect
from . import models
#from . import forms
from .forms import BookingForm

def StudentBooking(response):
    #response.user
    submitted = False
    if response.method == "POST":
        form = BookingForm(response.POST)
        if form.is_valid():
            #n= form.cleaned_data["name"]
            #t = Club(name=n)
            #t.save() 
            form.save()
            #response.user.clubname.add(t)
            return HttpResponseRedirect("/customer/booking?submitted=True")
    else:
        form = BookingForm()

        if 'submitted' in response.GET:
            submitted = True
        return render(response, "customer/booking.html", {'form':form, 'submitted':submitted})




























# from django.shortcuts import render
# from datetime import datetime

# from django.contrib.auth import authenticate
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect

# # Create your views here.
# from django.http import HttpResponse
# from django.views.generic import TemplateView

# from .models import Theatre, TicketBooking
# from django.db.models import Q
# from .models import ShowingItem
# from .forms import TicketBookingFormCreditCard, TicketBookingFormClub

# # Create your views here.


# class BookTicket(TemplateView):
#     template_name = "ticket_booking.html"

#     def post(self, request, *args, **kwargs):
#         print (request.POST)
#         print(args)
#         print(kwargs)

#         current_user = self.request.user
#         print(current_user.role)
#         if current_user.role == 2:
#             ticket_data = TicketBookingFormClub(request.POST)
#             if ticket_data.is_valid():
#                 print("data valid")
#                 show = showing.objects.get(id=kwargs['show_item'])
#                 ticket_date = datetime.strptime(request.POST["ticket_date"], '%d/%m/%Y')
#                 tickets = TicketBooking.objects.filter(showing=show, ticket_date=datetime.strftime(ticket_date, "%Y-%m-%d"))
#                 total = 0
#                 for tic in tickets:
#                     total = total + int(tic.ticket_count)

#                 print(total)

#                 if total + int(request.POST["number_of_tickets"]) > show.total_tickets:
#                     return HttpResponse("Not enough tickets , please try with a smaller number")
#                 user = authenticate(username=request.POST["user_name"], password=request.POST["pass_word"])
#                 if user is None:
#                     return HttpResponse("Incorrect credentials")
#                 my_ticket = TicketBooking()
#                 my_ticket.ticket_date = ticket_date
#                 my_ticket.ticket_type = 1
#                 my_ticket.ticket_count = request.POST["number_of_tickets"]
#                 my_ticket.buyer = self.request.user
#                 my_ticket.status = "ok"
#                 my_ticket.showing = show
#                 my_ticket.save()
#                 return HttpResponse("Data submitted successfully")

#             else:
#                 context = self.get_context_data(**kwargs)
#                 context['form'] = ticket_data
#                 return self.render_to_response(context)

#         else:
#             ticket_data = TicketBookingFormCreditCard(request.POST)
#             if ticket_data.is_valid():
#                 #check for number of tickets
#                 print("data valid")
#                 show = ShowingItem.objects.get(id=kwargs['show_item'])
#                 ticket_date = datetime.strptime(request.POST["ticket_date"], '%d/%m/%Y')
#                 tickets = TicketBooking.objects.filter(showing=show,
#                                                        ticket_date=datetime.strftime(ticket_date, "%Y-%m-%d"))
#                 total = 0
#                 for tic in tickets:
#                     total = total + int(tic.ticket_count)

#                 if total + int(request.POST["number_of_tickets"]) > show.total_tickets:
#                     return HttpResponse("Not enough tickets , please try with a smaller number")

#                 my_ticket = TicketBooking()
#                 my_ticket.ticket_date = ticket_date
#                 my_ticket.ticket_type = request.POST["ticket_type"]
#                 my_ticket.ticket_count = request.POST["number_of_tickets"]
#                 my_ticket.buyer = self.request.user
#                 my_ticket.status = "ok"
#                 my_ticket.showing = show
#                 my_ticket.credit_card_info = request.POST["credit_card_info"]
#                 my_ticket.credit_card_name = request.POST["credit_card_name"]
#                 my_ticket.credit_card_exp = request.POST["credit_card_year"] + "/" + request.POST["credit_card_month"]
#                 my_ticket.save()
#                 return HttpResponse("Data submitted successfully")
#             else:
#                 print("data invalid")

#                 context = self.get_context_data(**kwargs)
#                 context['form'] = ticket_data
#                 return self.render_to_response(context)

#             return HttpResponse("Data submitted successfully")

#         context = self.get_context_data(**kwargs)
#         context['form'] = ticket_data
#         return self.render_to_response(context)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         current_user = self.request.user
#         print(current_user.role)
#         if current_user.role == 2:
#             context['form'] = TicketBookingFormClub()
#             context['action'] = "confirm_club"
#         else:
#             context['form'] = TicketBookingFormCreditCard()
#             context['action'] = "confirm"

#         return context