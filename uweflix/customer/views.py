from django.shortcuts import render, redirect, get_object_or_404
import re
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from accounts.models import User
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
    version = int(request.GET['version'])


    # saving bookiong depending on booking button
    if version == 1:
        # getting form information
        adult_tickets = int(request.GET['adult'])
        student_tickets = int(request.GET['student'])
        child_tickets = int(request.GET['child'])
        showing_id = int(request.GET['showing_id'])
        id = int(request.GET['id'])
        print(version, adult_tickets,child_tickets,showing_id)
        # getting showing 
        showing = CinemaManager.get_showing(showing_id)
        # retrieving the user id that is logged in 
        user = User.objects.get(id=id)
        booking = Booking(showing=showing, student_tickets=student_tickets, child_tickets=child_tickets, adult_tickets=adult_tickets,user=user) #, total_price=total_price)
        booking.save()
        # for emailing ticket
        request.session['boooking_id'] = str(booking.bookingID)
        # deleting booking version
        del request.session['version']
    # club rep payment version    
    elif version ==2 :

        cr = request.session['cr']
        showing_id = request.session['showing_info']
        current_user = request.user
        showing = CinemaManager.get_showing(showing_id)
        # retrieving the user id that is logged in 
        user = User.objects.get(id=request.session['id'])
        booking = Booking.objects.create(showing=showing, cr_tickets=cr, user=user)
        request.session['boooking_id'] = str(booking.bookingID)
        del request.session['version']
    elif version == 4:
        # getting form information
        

        adult_tickets = int(request.GET['adult'])

        child_tickets = int(request.GET['child'])
        showing_id = int(request.GET['showing_id'])
        id = int(request.GET['id'])
        # getting showing 
        showing = CinemaManager.get_showing(showing_id)
        # retrieving the user id that is logged in 
        if id != None:
            user = User.objects.get(id=id)
            booking = Booking(showing=showing, child_tickets=child_tickets, adult_tickets=adult_tickets,user=user) #, total_price=total_price)
            booking.save()
        else:
            booking = Booking(showing=showing, child_tickets=child_tickets, adult_tickets=adult_tickets) #, total_price=total_price)
            booking.save()
        # for emailing ticket
        request.session['boooking_id'] = str(booking.bookingID)
        # deleting booking version
        del request.session['version']

        if version == 5:
            # getting form information
            adult_tickets = int(request.GET['adult'])
            child_tickets = int(request.GET['child'])
            showing_id = int(request.GET['showing_id'])
            id = int(request.GET['id'])
            print(version, adult_tickets,child_tickets,showing_id)
            # getting showing 
            showing = CinemaManager.get_showing(showing_id)
            # retrieving the user id that is logged in 
            user = User.objects.get(id=id)
            booking = Booking(showing=showing, child_tickets=child_tickets, adult_tickets=adult_tickets,user=user) #, total_price=total_price)
            booking.save()
            # for emailing ticket
            request.session['boooking_id'] = str(booking.bookingID)
            # deleting booking version
            del request.session['version']
    else:
        # to save the settling payment information
        pass
        #return view balance.

    return render(request, "customer/sucess.html")

@csrf_exempt
def sendmaill(request):
    send_mail("Booking Confirmation","Hello,\n\nThank you for your booking. \nThe confirmation ID is: "+request.session.get('boooking_id')+".\n\nKind regards,\nUWEFlix Team.","uweflix6@gmail.com",[request.POST.get('email')], fail_silently=False)
    return redirect('home')

# cancel page
@csrf_exempt
def cancel(request):
    version = request.session['version']
    if version == 1:
        del request.session['adult']
        del request.session['student']
        del request.session['child']
        del request.session['version']
    else:
        del request.session['cr']
        del request.session['version'] # version of booking 

   
    
    return render(request, "customer/cancel.html")

# stripe payment
@csrf_exempt

def pay(request):
    #booking = Booking.objects.get(pk=booking_id)
    version = request.session['version']
    #id = 1
    #user_id= request.session['id']
    showing_id = request.session['showing_info']

    if version == 1:
        user_id= request.session['id']
        adults = request.session['adult']
        student = request.session['student']
        child = request.session['child']
        #cr = request.session['cr']

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
        # if(cr > 0 ):
        #     items+= [{
        #         "price": "price_1MwnZwKummhyRPIWTUSuVw01",
        #         "quantity": cr,
        #         }]
        # del request.session['adult']
        # del request.session['student']
        # del request.session['child']
        # del request.session['cr']
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'], 
            line_items=items,   
            mode='payment',
            success_url= f'http://127.0.0.1:8000/customer/sucess/?version={version}&adult={adults}&child={child}&student={student}&id={user_id}&showing_id={showing_id}',
            cancel_url= 'http://127.0.0.1:8000/customer/cancel/',
            )
        return redirect(checkout_session.url)

    ############## club rep version #####################
    elif version == 2:
        user_id= request.session['id']
        cr = request.session['cr']
        items=[]

        if(cr > 0 ):
            items+= [{
                "price": "price_1MwnZwKummhyRPIWTUSuVw01",
                "quantity": cr,
                }]

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'], 
            line_items=items,   
            mode='payment',
            success_url= 'http://127.0.0.1:8000/customer/sucess/', 
            cancel_url= 'http://127.0.0.1:8000/customer/cancel/',
            
            )
        return redirect(checkout_session.url)
    
    ########### guest version ###############
    elif version == 4:
        adults = request.session['adult']
        child = request.session['child']
        items=[]
        if(adults > 0):
            items += [{
                "price": "price_1MrLtCKummhyRPIWtVsccm4O",
                "quantity": adults,
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
            success_url= f'http://127.0.0.1:8000/customer/sucess/?version={version}&adult={adults}&child={child}&showing_id={showing_id}', 
            cancel_url= 'http://127.0.0.1:8000/customer/cancel/',
            
            )
        return redirect(checkout_session.url)

    elif version == 5:
        user_id= request.session['id']
        adults = request.session['adult']
        child = request.session['child']
        items=[]
        if(adults > 0):
            items += [{
                "price": "price_1MrLtCKummhyRPIWtVsccm4O",
                "quantity": adults,
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
            success_url= f'http://127.0.0.1:8000/customer/sucess/?version={version}&id={user_id}&adult={adults}&child={child}&showing_id={showing_id}', 
            cancel_url= 'http://127.0.0.1:8000/customer/cancel/',
            
            )
        return redirect(checkout_session.url)

    else:

        #cr = request.session['cr']
        user_id= request.session['id']
        items=[]

        
        items+= [{
            "price": "price_1MwospKummhyRPIWFz1IxOIy",
            "quantity": 1,
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
