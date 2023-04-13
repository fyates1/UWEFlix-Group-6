from django.shortcuts import render, redirect, get_object_or_404
import re
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from .forms import BookingForm
import stripe
from django.conf import settings
from cinema.models import Booking
from django.contrib.sessions.models import Session
from cinema.views import CinemaManager
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY

# booking form
def StudentBooking(response):
    #response.user
    submitted = False
    if response.method == "POST":
        form = BookingForm(response.POST)
        if form.is_valid():

            form.save()
            return HttpResponseRedirect("/customer/booking?submitted=True")
    else:
        form = BookingForm()
        if 'submitted' in response.GET:
            submitted = True
        return render(response, "customer/booking.html", {'form':form, 'submitted':submitted})


# checkout rendering
def landing(response):
    pass
    return render(response, "customer/checkout.html")

# sucess page where the booking gets saved
@csrf_exempt
def sucess(request):

    adult_tickets = request.session['adult']
    student_tickets = request.session['student']
    child_tickets = request.session['child']
    showing_id = request.session['showing_info']
    showing = CinemaManager.get_showing(showing_id)
    booking = Booking(showing=showing, student_tickets=student_tickets, child_tickets=child_tickets, adult_tickets=adult_tickets) #, total_price=total_price)
    booking.save()
    request.session['boooking_id'] = str(booking.bookingID)
    return render(request, "customer/sucess.html")

@csrf_exempt
def sendmaill(request):
    send_mail("Booking Confirmation","Hello,\n\nThank you for your booking. \nThe confirmation ID is: "+request.session.get('boooking_id')+".\n\nKind regards,\nUWEFlix Team.","uweflix6@gmail.com",[request.POST.get('email')], fail_silently=False)
    return redirect('home')

# cancel page
@csrf_exempt
def cancel(response):
    pass
    return render(response, "customer/cancel.html")

# stripe payment
@csrf_exempt
def pay(request):
    #booking = Booking.objects.get(pk=booking_id)
    adults = request.session['adult']
    student = request.session['student']
    child = request.session['child']
    #DOMAIN ='http://127.0.0.1:8000/customer/',
    items=[]
    if(adults > 0):
        items += [{
            "price": "price_1MrLtCKummhyRPIWtVsccm4O",
            "quantity": adults,
            }]
    if(student > 0 ):
        items += [{
            "price": "price_1MrLtaKummhyRPIWQbNz4wn6",
            "quantity": student,
            }]
    if(child > 0 ):
        items += [{
            "price": "price_1MrLvzKummhyRPIW8U9BAMmJ",
            "quantity": child,
            }]
    
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'], 
        line_items=items,   
        mode='payment',
        success_url= 'http://127.0.0.1:8000/customer/sucess/', # will be changed later to proper url
        cancel_url= 'http://127.0.0.1:8000/customer/cancel/',
        
        )
    return redirect(checkout_session.url)

#testing card details for stripe
#number : 4242 4242 4242 4242
# 04/23 
# 123
#




























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
