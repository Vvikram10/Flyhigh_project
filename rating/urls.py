from django.urls import path
from .import views

urlpatterns = [
    path('add_review/', views.add_review, name='add_review'),
    path('view_review/', views.view_review, name='view_review'),
    path('review_dashboard/', views.review_dashboard, name='review_dashboard'),
]
