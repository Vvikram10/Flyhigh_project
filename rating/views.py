from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .models import ReviewRating

# @login_required
def add_review(request):
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

        return redirect('add_review')  # Redirect to a success page or another view

    # Fetch the existing review for the user and subject (if any) to pre-fill the form
    user = request.user
    subject = request.GET.get('subject')  # Get subject from query parameters
    existing_review = ReviewRating.objects.filter(user=user, subject=subject).first()

    return render(request, 'rating/add_review.html', {
        'username': user.first_name,
        'existing_review': existing_review,
    })

# @login_required
# def view_review(request):
#     # Fetch all reviews for the authenticated user
#     user = request.user
#     existing_reviews = ReviewRating.objects.filter(user=user).all()

#     return render(request, 'rating/view_reviews.html', {
#         'username': user.first_name,
#         'existing_reviews': existing_reviews,
#     })

def view_review(request):
    reviews = ReviewRating.objects.filter(status=True).select_related('user')   # Filter to show only approved reviews
    context = {
        'existing_reviews': reviews,
    }
    return render(request, 'rating/view_review.html', context)


from django.db.models import Avg, Count

def review_dashboard(request):
    # Fetch all review ratings
    rating_counts = [
        {'rating': 1, 'count': ReviewRating.objects.filter(rating=1).count()},
        {'rating': 2, 'count': ReviewRating.objects.filter(rating=2).count()},
        {'rating': 3, 'count': ReviewRating.objects.filter(rating=3).count()},
        {'rating': 4, 'count': ReviewRating.objects.filter(rating=4).count()},
        {'rating': 5, 'count': ReviewRating.objects.filter(rating=5).count()},
    ]

    context = {
        'rating_counts': rating_counts,
        'reviews': ReviewRating.objects.all(),
    }
    return render(request, 'admin/review_dashboard.html', context)