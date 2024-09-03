from django.contrib import admin
from .models import ReviewRating, CustomerDetails

@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'subject', 'rating', 'status', 'created_at', 'updated_at')
