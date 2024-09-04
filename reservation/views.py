from email.message import EmailMessage
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import json
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ClassMaster, CompanyMaster, AerodrumMaster, DayMaster, FlightMaster, FlightFareMap, FlightDayMap, CustomerDetails

# ClassMaster Views
def class_list(request):
    classes = ClassMaster.objects.all()
    return render(request, 'class/class_list.html', {'classes': classes})

def class_create(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        if class_name:
            ClassMaster.objects.create(class_name=class_name)
            return redirect('class_list')
        else:
            return HttpResponseBadRequest("Invalid data")
    return render(request, 'class/class_form.html', {'title': 'Create Class'})

def class_update(request, pk):
    class_ = get_object_or_404(ClassMaster, pk=pk)
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        if class_name:
            class_.class_name = class_name
            class_.save()
            return redirect('class_list')
        else:
            return HttpResponseBadRequest("Invalid data")
    return render(request, 'class/class_form.html', {'class': class_, 'title': 'Update Class'})

def class_delete(request, pk):
    class_ = get_object_or_404(ClassMaster, pk=pk)
    if request.method == 'POST':
        class_.delete()
        return redirect('class_list')
    return render(request, 'class/confirm_delete.html', {'object': class_})

# CompanyMaster Views
def company_list(request):
    companies = CompanyMaster.objects.all()
    return render(request, 'company/company_list.html', {'companies': companies})

def company_create(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        if company_name:
            CompanyMaster.objects.create(company_name=company_name)
            return redirect('company_list')
        else:
            return HttpResponseBadRequest("Invalid data")
    return render(request, 'company/company_form.html', {'title': 'Create Company'})

def company_update(request, pk):
    company = get_object_or_404(CompanyMaster, pk=pk)
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        if company_name:
            company.company_name = company_name
            company.save()
            return redirect('company_list')
        else:
            return HttpResponseBadRequest("Invalid data")
    return render(request, 'company/company_form.html', {'company': company, 'title': 'Update Company'})

def company_delete(request, pk):
    company = get_object_or_404(CompanyMaster, pk=pk)
    if request.method == 'POST':
        company.delete()
        return redirect('company_list')
    return render(request, 'company/confirm_delete.html', {'object': company})

# AerodrumMaster Views
def aerodrum_list(request):
    aerodrums = AerodrumMaster.objects.all()
    return render(request, 'aerodrum/aerodrum_list.html', {'aerodrums': aerodrums})

def aerodrum_create(request):
    if request.method == 'POST':
        aerodrum_name = request.POST.get('aerodrum_name')
        city = request.POST.get('city')
        state = request.POST.get('state')
        if aerodrum_name and city and state:
            AerodrumMaster.objects.create(aerodrum_name=aerodrum_name, city=city, state=state)
            return redirect('aerodrum_list')
        else:
            return HttpResponseBadRequest("Invalid data")
    return render(request, 'aerodrum/aerodrum_form.html', {'title': 'Create Aerodrum'})

def aerodrum_update(request, pk):
    aerodrum = get_object_or_404(AerodrumMaster, pk=pk)
    if request.method == 'POST':
        aerodrum_name = request.POST.get('aerodrum_name')
        city = request.POST.get('city')
        state = request.POST.get('state')
        if aerodrum_name and city and state:
            aerodrum.aerodrum_name = aerodrum_name
            aerodrum.city = city
            aerodrum.state = state
            aerodrum.save()
            return redirect('aerodrum_list')
        else:
            return HttpResponseBadRequest("Invalid data")
    return render(request, 'aerodrum/aerodrum_form.html', {'aerodrum': aerodrum, 'title': 'Update Aerodrum'})

def aerodrum_delete(request, pk):
    aerodrum = get_object_or_404(AerodrumMaster, pk=pk)
    if request.method == 'POST':
        aerodrum.delete()
        return redirect('aerodrum_list')
    return render(request, 'aerodrum/confirm_delete.html', {'object': aerodrum})

# DayMaster Views
def day_list(request):
    days = DayMaster.objects.all()
    return render(request, 'day/day_list.html', {'days': days})

def day_create(request):
    if request.method == 'POST':
        day_name = request.POST.get('day_name')
        if day_name:
            DayMaster.objects.create(day_name=day_name)
            return redirect('day_list')
        else:
            return HttpResponseBadRequest("Invalid data")
    return render(request, 'day/day_form.html', {'title': 'Create Day'})

def day_update(request, pk):
    day = get_object_or_404(DayMaster, pk=pk)
    if request.method == 'POST':
        day_name = request.POST.get('day_name')
        if day_name:
            day.day_name = day_name
            day.save()
            return redirect('day_list')
        else:
            return HttpResponseBadRequest("Invalid data")
    return render(request, 'day/day_form.html', {'day': day, 'title': 'Update Day'})

def day_delete(request, pk):
    day = get_object_or_404(DayMaster, pk=pk)
    if request.method == 'POST':
        day.delete()
        return redirect('day_list')
    return render(request, 'day/confirm_delete.html', {'object': day})

# FlightMaster Views
def flight_list(request):
    flights = FlightMaster.objects.all()
    return render(request, 'flight/flight_list.html', {'flights': flights})

def flight_create(request):
    if request.method == 'POST':
        flight_name = request.POST.get('flight_name')
        company_id = request.POST.get('company')
        source_id = request.POST.get('source')
        destination_id = request.POST.get('destination')
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')
        if flight_name and company_id and source_id and destination_id and departure_time and arrival_time:
            FlightMaster.objects.create(
                flight_name=flight_name,
                company_id=company_id,
                source_id=source_id,
                destination_id=destination_id,
                departure_time=departure_time,
                arrival_time=arrival_time
            )
            return redirect('flight_list')
        else:
            return HttpResponseBadRequest("Invalid data")
    
    companies = CompanyMaster.objects.all()
    aerodrums = AerodrumMaster.objects.all()
    return render(request, 'flight/flight_form.html', {
        'title': 'Create Flight',
        'companies': companies,
        'aerodrums': aerodrums
    })

def flight_update(request, pk):
    flight = get_object_or_404(FlightMaster, pk=pk)
    if request.method == 'POST':
        flight_name = request.POST.get('flight_name')
        company_id = request.POST.get('company')
        source_id = request.POST.get('source')
        destination_id = request.POST.get('destination')
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')
        if flight_name and company_id and source_id and destination_id and departure_time and arrival_time:
            flight.flight_name = flight_name
            flight.company_id = company_id
            flight.source_id = source_id
            flight.destination_id = destination_id
            flight.departure_time = departure_time
            flight.arrival_time = arrival_time
            flight.save()
            return redirect('flight_list')
        else:
            return HttpResponseBadRequest("Invalid data")
    
    companies = CompanyMaster.objects.all()
    aerodrums = AerodrumMaster.objects.all()
    return render(request, 'flight/flight_form.html', {
        'flight': flight,
        'title': 'Update Flight',
        'companies': companies,
        'aerodrums': aerodrums
    })

def flight_delete(request, pk):
    flight = get_object_or_404(FlightMaster, pk=pk)
    if request.method == 'POST':
        flight.delete()
        return redirect('flight_list')
    return render(request, 'flight/confirm_delete.html', {'object': flight})

# FlightFareMap Views
def flight_fare_map_list(request):
    flight_fares = FlightFareMap.objects.all()
    return render(request, 'faremap/flight_fare_map_list.html', {'flight_fares': flight_fares})

def flight_fare_map_create(request):
    if request.method == 'POST':
        flight_id = request.POST.get('flight')
        flight_class_id = request.POST.get('flight_class')
        no_of_seats = request.POST.get('no_of_seats')
        fare = request.POST.get('fare')
        if flight_id and flight_class_id and no_of_seats and fare:
            FlightFareMap.objects.create(
                flight_id=flight_id,
                flight_class_id=flight_class_id,
                no_of_seats=no_of_seats,
                fare=fare
            )
            return redirect('flight_fare_map_list')
        else:
            return HttpResponseBadRequest("Invalid data")
    
    # Fetch flights and flight classes to populate the dropdowns
    flights = FlightMaster.objects.all()
    flight_classes = ClassMaster.objects.all()  # Adjust the model name if necessary
    
    return render(request, 'faremap/flight_fare_map_form.html', {
        'title': 'Create Flight Fare Map',
        'flights': flights,
        'flight_classes': flight_classes
    })


def flight_fare_map_update(request, pk):
    flight_fare_map = get_object_or_404(FlightFareMap, pk=pk)
    if request.method == 'POST':
        flight_id = request.POST.get('flight')
        flight_class_id = request.POST.get('flight_class')
        no_of_seats = request.POST.get('no_of_seats')
        fare = request.POST.get('fare')
        if flight_id and flight_class_id and no_of_seats and fare:
            flight_fare_map.flight_id = flight_id
            flight_fare_map.flight_class_id = flight_class_id
            flight_fare_map.no_of_seats = no_of_seats
            flight_fare_map.fare = fare
            flight_fare_map.save()
            return redirect('flight_fare_map_list')
        else:
            return HttpResponseBadRequest("Invalid data")
    
    # Fetch flights and flight classes to populate the dropdowns
    flights = FlightMaster.objects.all()
    flight_classes = ClassMaster.objects.all()  # Adjust the model name if necessary
    
    return render(request, 'faremap/flight_fare_map_form.html', {
        'title': 'Update Flight Fare Map',
        'fare_map': flight_fare_map,
        'flights': flights,
        'flight_classes': flight_classes
    })

def flight_fare_map_delete(request, pk):
    flight_fare_map = get_object_or_404(FlightFareMap, pk=pk)
    if request.method == 'POST':
        flight_fare_map.delete()
        return redirect('flight_fare_map_list')
    return render(request, 'faremap/confirm_delete.html', {'object': flight_fare_map})

# FlightDayMap Views
def flight_day_map_list(request):
    flight_days = FlightDayMap.objects.all()
    return render(request, 'faremap/flight_day_map_list.html', {'flight_days': flight_days})

def flight_day_map_create(request):
    if request.method == 'POST':
        flight_id = request.POST.get('flight')
        day_id = request.POST.get('day')

        # Ensure that flight_id and day_id are provided
        if not (flight_id and day_id):
            return HttpResponseBadRequest("Missing data in the request")

        try:
            # Ensure that the IDs correspond to existing objects
            flight = FlightMaster.objects.get(pk=flight_id)
            day = DayMaster.objects.get(pk=day_id)
        except FlightMaster.DoesNotExist:
            return HttpResponseBadRequest("Invalid flight ID")
        except DayMaster.DoesNotExist:
            return HttpResponseBadRequest("Invalid day ID")

        try:
            # Create the new FlightDayMap record
            FlightDayMap.objects.create(flight=flight, day=day)
            return redirect('flight_day_map_list')
        except Exception as e:
            return HttpResponseBadRequest(f"Error creating FlightDayMap: {str(e)}")

    # Fetch all flights and days to populate the form dropdowns
    flights = FlightMaster.objects.all()
    days = DayMaster.objects.all()
    
    return render(request, 'faremap/flight_day_map_form.html', {
        'title': 'Create Flight Day Map',
        'flights': flights,
        'days': days
    })



def flight_day_map_update(request, pk):
    flight_day_map = get_object_or_404(FlightDayMap, pk=pk)
    if request.method == 'POST':
        flight_id = request.POST.get('flight')
        day_id = request.POST.get('day')
       
        if flight_id and day_id :
            flight_day_map.flight_id = flight_id
            flight_day_map.day_id = day_id
            
            flight_day_map.save()
            return redirect('flight_day_map_list')
        else:
            return HttpResponseBadRequest("Invalid data")
    
    flights = FlightMaster.objects.all()
    days = DayMaster.objects.all()
    return render(request, 'faremap/flight_day_map_form.html', {
        'flight_day_map': flight_day_map,
        'flights': flights,
        'days': days,
        'title': 'Update Flight Day Map'
    })

def flight_day_map_delete(request, pk):
    flight_day_map = get_object_or_404(FlightDayMap, pk=pk)
    if request.method == 'POST':
        flight_day_map.delete()
        return redirect('flight_day_map_list')
    return render(request, 'class/confirm_delete.html', {'object': flight_day_map})


def search_flights(request):
    source_name = request.GET.get('source', '')
    destination_name = request.GET.get('destination', '')

    flights = FlightMaster.objects.all()
    
    if source_name:
        flights = flights.filter(source__city__icontains=source_name)
    if destination_name:
        flights = flights.filter(destination__city__icontains=destination_name)

    return render(request, 'flight/search_flights.html', {'flights': flights})

    
@login_required
def check_availability(request, flight_id):
    flight = get_object_or_404(FlightMaster, flight_no=flight_id)
    seat_maps = FlightFareMap.objects.filter(flight=flight)
    
    availability = []
    
    for seat_map in seat_maps:
        # Retrieve all booked seats for this flight and class
        booked_seat_numbers = seat_map.booked_seats
        
        # Calculate available seats
        total_seats = seat_map.no_of_seats
        booked_seats_count = len(booked_seat_numbers)
        available_seats = total_seats - booked_seats_count
        
        availability.append({
            'class_name': seat_map.flight_class.class_name,
            'total_seats': total_seats,
            'booked_seats': booked_seats_count,
            'available_seats': available_seats,
            'fare': seat_map.fare,
            'flight_class_id': seat_map.flight_class.class_id,
            'booked_seat_numbers': booked_seat_numbers,  # Add booked seat numbers
        })

    return render(request, 'flight/check_availability.html', {
        'flight': flight,
        'availability': availability,
    })


@login_required
def cancel_ticket(request, pnr_number):
    ticket = get_object_or_404(CustomerDetails, pnr_number=pnr_number)
    
    if request.method == 'POST':
        # Mark the ticket as canceled
        ticket.status = 'Cancel'
        ticket.is_reserved = False
        seat_number = ticket.seat_number
        flight = ticket.flight
        flight_class = ticket.flight_class

        # Remove the seat number from the booked_seats list
        seat_map = get_object_or_404(FlightFareMap, flight=flight, flight_class=flight_class)
        if seat_number in seat_map.booked_seats:
            seat_map.booked_seats.remove(seat_number)
            seat_map.save()

        # Save the updated ticket status
        ticket.save()
        print(f"Ticket status after save: {ticket.status}")  # Debugging line
        
        try:
            # Send cancellation confirmation email
            mail_subject = 'Your Ticket Cancellation Confirmation'
            message = render_to_string('customer/cancel_confirmation_email.html', {
                'user': request.user,
                'booking': ticket,
                'flight': ticket.flight,
                'flight_class': ticket.flight_class,
                'total': ticket.total,
                'tax': ticket.tax,
                'grand_total': ticket.fare_total,
                'pnr_number': ticket.pnr_number,
                'seat_numbers': ticket.seat_number,
                'payment': ticket.payment,
                'source': ticket.flight.source.aerodrum_name,
                'destination': ticket.flight.destination.aerodrum_name,
                'departure_time': ticket.flight.departure_time,
                'arrival_time': ticket.flight.arrival_time,
            })
            to_email = request.user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            print("Email sent successfully")
        except Exception as e:
            print(f"Error sending email: {e}")

        # Redirect to an appropriate page after cancellation
        return redirect('search_ticket')
    
    return render(request, 'customer/cancel_ticket.html', {'ticket': ticket})






# CustomerDetails Views
def customer_details_list(request):
    customers = CustomerDetails.objects.all()
    return render(request, 'customer/customer_details_list.html', {'customers': customers})

def customer_details_create(request):
    if request.method == 'POST':
        passport_id = request.POST.get('passport_id')
        customer_name = request.POST.get('customer_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        email_id = request.POST.get('email_id')
        contact_no = request.POST.get('contact_no')
        booking_date = request.POST.get('booking_date')
        flight_class_id = request.POST.get('flight_class')
        flight_id = request.POST.get('flight')

        if passport_id and customer_name and age and gender and city and email_id and contact_no and booking_date and flight_class_id and flight_id:
            CustomerDetails.objects.create(
                passport_id=passport_id,
                customer_name=customer_name,
                age=age,
                gender=gender,
                city=city,
                email_id=email_id,
                contact_no=contact_no,
                booking_date=booking_date,
                flight_class_id=flight_class_id,
                flight_id=flight_id
            )
            return redirect('customer_details_list')
        else:
            return HttpResponseBadRequest("Invalid data")

    # Fetch all flight classes and flights for the form dropdowns
    classes = ClassMaster.objects.all()
    flights = FlightMaster.objects.all()

    return render(request, 'customer/customer_details_form.html', {
        'title': 'Create Customer Details',
        'classes': classes,
        'flights': flights
    })


def customer_details_update(request, pk):
    customer = get_object_or_404(CustomerDetails, pk=pk)
    if request.method == 'POST':
        passport_id = request.POST.get('passport_id')
        customer_name = request.POST.get('customer_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        email_id = request.POST.get('email_id')
        contact_no = request.POST.get('contact_no')
        booking_date = request.POST.get('booking_date')
        flight_class_id = request.POST.get('flight_class')
        flight_id = request.POST.get('flight')
        if passport_id and customer_name and age and gender and city and email_id and contact_no and booking_date and flight_class_id and flight_id:
            customer.passport_id = passport_id
            customer.customer_name = customer_name
            customer.age = age
            customer.gender = gender
            customer.city = city
            customer.email_id = email_id
            customer.contact_no = contact_no
            customer.booking_date = booking_date
            customer.flight_class_id = flight_class_id
            customer.flight_id = flight_id
            customer.save()
            return redirect('customer_details_list')
        else:
            return HttpResponseBadRequest("Invalid data")
    return render(request, 'customer/customer_details_form.html', {'customer': customer, 'title': 'Update Customer Details'})

def customer_details_delete(request, pk):
    customer = get_object_or_404(CustomerDetails, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_details_list')
    return render(request, 'confirm_delete.html', {'object': customer})


from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import CustomerDetails, FlightMaster, ClassMaster, FlightFareMap
import random
import uuid


@login_required
def book_ticket(request, flight_no, flight_class_id):
    current_user = request.user
    if not current_user.is_authenticated:
        return redirect('login')

    flight = get_object_or_404(FlightMaster, flight_no=flight_no)
    flight_class = get_object_or_404(ClassMaster, class_id=flight_class_id)
    seat_map = get_object_or_404(FlightFareMap, flight=flight, flight_class=flight_class)
    total = seat_map.fare
    tax = (18 * total) / 100
    grand_total = total + tax
    
    if request.method == 'POST':
        passport_id = request.POST.get('passport_id')
        customer_name = request.POST.get('customer_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        booking_date = request.POST.get('booking_date')
        email_id = request.POST.get('email_id')
        contact_no = request.POST.get('contact_no')
        country = request.POST.get('country')

        if not passport_id:
            return render(request, 'customer/book_ticket.html', {
                'flight': flight,
                'flight_class': flight_class,
                'error': 'Passport ID is required.',
            })

        # Generate seat number based on class name
        booked_seats_count = len(seat_map.booked_seats)
        seat_prefix = flight_class.class_name[0].upper()  # e.g., 'P' for Premium
        seat_number = f"{seat_prefix}{booked_seats_count + 1}"

        # Add seat number to booked seats
        seat_map.booked_seats.append(seat_number)
        seat_map.save()

        booking_instance = CustomerDetails(
            user=current_user,
            passport_id=passport_id,
            customer_name=customer_name,
            age=age,
            gender=gender,
            city=city,
            email_id=email_id,
            contact_no=contact_no,
            booking_date=booking_date,
            flight_class=flight_class,
            flight=flight,
            country=country,
            total=total,
            fare_total=grand_total,
            tax=tax,
            status='Pending',
            is_reserved=False,
            short_token=uuid.uuid4(),
            seat_number=seat_number,
        )
        booking_instance.pnr_number = generate_unique_pnr()
        booking_instance.save()
        
        return redirect('payment', short_token=booking_instance.short_token)
    
    context = {
        'flight': flight,
        'flight_class': flight_class,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
        'seat_map': seat_map
    }
    return render(request, 'customer/book_ticket.html', context)


def generate_unique_pnr():
    """Generate a unique 14-digit PNR number based on current datetime and a random number."""
    while True:
        now = timezone.now()
        pnr_base = now.strftime('%Y%m%d%H%M')  # YYYYMMDDHHMM format
        random_number = random.randint(1000, 9999)  # 4-digit random number
        pnr_number = f"{pnr_base}{random_number}"
        
        if not CustomerDetails.objects.filter(pnr_number=pnr_number).exists():
            return pnr_number



from django.shortcuts import render, get_object_or_404, redirect
from .models import Payment, CustomerDetails
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

@login_required
def payment(request, short_token):
    booking = get_object_or_404(CustomerDetails, short_token=short_token)
    flight = booking.flight  # Access the flight from the booking

    # Assuming 'source' and 'destination' are the field names in your FlightMaster model
    flight_source = flight.source
    flight_destination = flight.destination

    # if request.method == 'POST':
    #     # Payment processing logic
    #     payment_id = request.POST.get('payment_id')
    #     payment_method = request.POST.get('payment_method')
    #     status = request.POST.get('status')
        
    #     # Save payment details
    #     payment_instance = Payment(
    #         user=request.user,
    #         payment_id=payment_id,
    #         payment_method=payment_method,
    #         amount_paid=booking.fare_total,
    #         status=status
    #     )
    #     payment_instance.save()
        
    #     # Update booking status
    #     booking.status = status
    #     booking.is_reserved = True  # Mark the seat as reserved
    #     booking.save()

        # Redirect to booking confirmation or a success page
        # return redirect('booking_confirmation', booking_id=booking.id)
    
    context = {
        'booking': booking,
        'flight': flight,
        'flight_class': booking.flight_class,
        'total': booking.total,
        'tax': booking.tax,
        'grand_total': booking.fare_total,
        'flight_source': flight_source,  # Include the flight source
        'flight_destination': flight_destination  # Include the flight destination
    }
    return render(request, 'customer/payment.html', context)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            
            # Debugging: Print raw data received
            print(f"Received raw data: {data}")
            
            # Retrieve order using orderID
            order = CustomerDetails.objects.get(user=request.user, is_reserved=False, pnr_number=data.get('orderID'))
            
            # Debugging: Print the retrieved order
            print(f"Retrieved order: {order}")
            
            # Extract fields from data
            short_token = data.get('short_token')
            trans_id = data.get('transID')
            payment_method = data.get('payment_method')
            status = data.get('status')
            
            # Debugging: Print the extracted fields
            print(f"Extracted data - short_token: {short_token}, transID: {trans_id}, payment_method: {payment_method}, status: {status}")
            
            # Find the booking using short_token
            booking = get_object_or_404(CustomerDetails, short_token=short_token)
            
            # Debugging: Print the booking
            print(f"Retrieved booking: {booking}")
            
            # Create and save Payment instance
            payment = Payment(
                user=request.user,  # Ensure request.user is available and valid
                payment_id=trans_id,
                payment_method=payment_method,
                amount_paid=booking.fare_total,
                status=status
            )
            payment.save()
            
            # Debugging: Print the saved payment instance
            print(f"Saved payment: {payment}")
            
            # Update the booking status
            order.status = status
            order.is_reserved = True
            order.save()
            
            # Return JSON response
            return JsonResponse({
                'order_number': booking.pnr_number,
                'transID': payment.payment_id
            })
        except Exception as e:
            print(f"Error processing payment: {e}")
            return JsonResponse({'error': str(e)}, status=400)



@login_required
def booking_confirmation(request, booking_id):
    # Retrieve the booking details
    booking = get_object_or_404(CustomerDetails, id=booking_id, user=request.user)

    # Retrieve pnr_number and transID from the GET request parameters
    pnr_number = request.GET.get('pnr_number')
    transID = request.GET.get('payment_id')

    # Validate if the provided pnr_number matches the booking's pnr_number
    error_message = None
    if pnr_number and pnr_number != booking.pnr_number:
        error_message = 'Invalid PNR number.'

    # Fetch the payment details based on transID (payment_id)
    payment = None
    if transID and not error_message:
        try:
            payment = Payment.objects.get(payment_id=transID, user=request.user)
        except Payment.DoesNotExist:
            error_message = 'Payment details not found.'

    # Get flight day from FlightDayMap
    flight_day = None
    try:
        flight_day_entry = FlightDayMap.objects.get(flight=booking.flight)
        flight_day = flight_day_entry.day.day_name  # Assuming day_name is what you want to display
    except FlightDayMap.DoesNotExist:
        flight_day = 'Not available'

    mail_subject = 'Thank you for your order!'
    message = render_to_string('customer/mail_recieved_email.html', {
        'user': request.user,
        'booking': booking,
        'flight': booking.flight,
        'flight_class': booking.flight_class,
        'total': booking.total,
        'tax': booking.tax,
        'grand_total': booking.fare_total,
        'pnr_number': booking.pnr_number,
        'seat_numbers': booking.seat_number,  # Assuming this is a single field
        'payment': payment,  # Include payment details in the context
        'error_message': error_message,  # Pass the error message to the template
        'source': booking.flight.source.aerodrum_name,  # Access aerodrum_name
        'destination': booking.flight.destination.aerodrum_name,  # Access aerodrum_name
        'departure_time': booking.flight.departure_time,
        'arrival_time': booking.flight.arrival_time,
        'flight_day': flight_day,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    context = {
        'booking': booking,
        'flight': booking.flight,
        'flight_class': booking.flight_class,
        'total': booking.total,
        'tax': booking.tax,
        'grand_total': booking.fare_total,
        'pnr_number': booking.pnr_number,
        'seat_numbers': booking.seat_number,  # Assuming this is a single field
        'payment': payment,  # Include payment details in the context
        'error_message': error_message,  # Pass the error message to the template
        'source': booking.flight.source.aerodrum_name,  # Access aerodrum_name
        'destination': booking.flight.destination.aerodrum_name,  # Access aerodrum_name
        'departure_time': booking.flight.departure_time,
        'arrival_time': booking.flight.arrival_time,
        'flight_day': flight_day,
    }

    return render(request, 'customer/booking_confirmation.html', context)



def reservation(request):
    # Fetch all orders sorted by booking date
    orders = CustomerDetails.objects.all().order_by('-booking_date')

    # Fetch data for the reserved status graph
    reserved_data = list(CustomerDetails.objects.values('is_reserved').annotate(count=Count('id')))

    # Calculate total number of PNRs
    total_pnrs = CustomerDetails.objects.count()

    context = {
        'orders': orders,
        'reserved_data': json.dumps(reserved_data),  # Convert to JSON
        'total_pnrs': total_pnrs,
    }
    return render(request, 'admin/reservation.html', context)