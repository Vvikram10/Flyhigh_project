from django.http import HttpResponseBadRequest
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reservation.models import *
from django.urls import reverse
from rating.models import ReviewRating

def nav(request):
    return render(request,'base/navbar.html')
def home(request):
    return render(request,'base/home.html')

def about(request):
    reviews = ReviewRating.objects.filter(status=True).select_related('user')   # Filter to show only approved reviews
    context = {
        'existing_reviews': reviews,
    }
    return render(request, 'base/about.html', context)

# def aboutpage(request):
#     return render(request,'base/aboutpage.html')
    
def service(request):
    return render(request,'base/service.html')

def contactpage(request):
    return render(request,'base/contactpage.html')

def contact(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        
        # The currently logged-in user
        user = request.user

        if not subject or not review or not rating:
            return HttpResponseBadRequest("Missing required fields")

        # Check if a review already exists for this user and subject
        existing_review = ReviewRating.objects.filter(user=user, subject=subject).first()

        if existing_review:
            # Update the existing review
            existing_review.review = review
            existing_review.rating = rating
            existing_review.save()
        else:
            # Create a new review
            review_rating = ReviewRating(
                user=user,
                name=user.first_name,  # Assuming you want to save the user's first name
                subject=subject,
                review=review,
                rating=rating,
            )
            review_rating.save()

        return redirect('contact')  # Redirect to a success page or another view

    # Fetch the existing review for the user and subject (if any) to pre-fill the form
    user = request.user
    subject = request.GET.get('subject')  # Get subject from query parameters
    existing_review = ReviewRating.objects.filter(user=user, subject=subject).first()

    return render(request, 'base/contact.html', {
        'username': user.first_name,
        'existing_review': existing_review,
    })
    




def search_flight(request):
    source_name = request.GET.get('source', '')
    destination_name = request.GET.get('destination', '')

    flights = FlightMaster.objects.all()
    
    if source_name:
        flights = flights.filter(source__city__icontains=source_name)
    if destination_name:
        flights = flights.filter(destination__city__icontains=destination_name)

    if flights.exists():
        # Redirect to the search results page if flights exist
        return redirect(reverse('search_flights') + f'?source={source_name}&destination={destination_name}')
    else:
        # If no flights are found, stay on the current page
        return render(request, 'base/home.html', {'message': 'No flights found. Please try again.'})
    
@login_required
def search_ticket(request):
    if request.method == 'POST':
        pnr_number = request.POST.get('pnr_number')
        if pnr_number:
            try:
                # Fetch the ticket by PNR number
                ticket = CustomerDetails.objects.get(pnr_number=pnr_number)

                # Check if the ticket is canceled
                if ticket.status == 'Cancel':
                    raise CustomerDetails.DoesNotExist  # Trigger the exception to show the error message
                
                return render(request, 'customer/ticket_found.html', {'ticket': ticket})
            except CustomerDetails.DoesNotExist:
                # Handle case where ticket is not found or is canceled
                messages.error(request, 'Ticket not found or has been canceled.', extra_tags='danger')
                return render(request, 'customer/search_ticket.html')
    return render(request, 'customer/search_ticket.html')



@login_required
def search_tickets(request):
    if request.method == 'POST':
        pnr_number = request.POST.get('pnr_number')
        if pnr_number:
            try:
                ticket = CustomerDetails.objects.get(pnr_number=pnr_number)
                return render(request, 'base/ticket_finds.html', {'ticket': ticket})
            except CustomerDetails.DoesNotExist:
                messages.error(request,'Ticket not found.',extra_tags='danger')
                return render(request, 'base/search_tickets.html')
    return render(request, 'base/search_tickets.html')
