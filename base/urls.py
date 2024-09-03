from django.urls import path
from . import views


urlpatterns = [
    path('nav/', views.nav, name='nav'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # path('aboutpage/', views.aboutpage, name='aboutpage'),
    path('service/', views.service, name='service'),
    path('contact/', views.contact, name='contact'),
    path('contactpage/', views.contactpage, name='contactpage'),
    path('search_flight/', views.search_flight, name='search_flight'),
    path('search-ticket/', views.search_ticket, name='search_ticket'),
    path('search-tickets/', views.search_tickets, name='search_tickets'),
   

]