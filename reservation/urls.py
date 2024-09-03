from django.urls import path
from . import views

urlpatterns = [
    # ClassMaster URLs
    path('classes/', views.class_list, name='class_list'),
    path('classes/create/', views.class_create, name='class_create'),
    path('classes/<int:pk>/update/', views.class_update, name='class_update'),
    path('classes/<int:pk>/delete/', views.class_delete, name='class_delete'),

    # CompanyMaster URLs
    path('companies/', views.company_list, name='company_list'),
    path('companies/create/', views.company_create, name='company_create'),
    path('companies/<int:pk>/update/', views.company_update, name='company_update'),
    path('companies/<int:pk>/delete/', views.company_delete, name='company_delete'),

     # AerodrumMaster URLs
    path('aerodrums/', views.aerodrum_list, name='aerodrum_list'),
    path('aerodrums/create/', views.aerodrum_create, name='aerodrum_create'),
    path('aerodrums/<int:pk>/update/', views.aerodrum_update, name='aerodrum_update'),
    path('aerodrums/<int:pk>/delete/', views.aerodrum_delete, name='aerodrum_delete'),

    # DayMaster URLs
    path('days/', views.day_list, name='day_list'),
    path('days/create/', views.day_create, name='day_create'),
    path('days/<int:pk>/update/', views.day_update, name='day_update'),
    path('days/<int:pk>/delete/', views.day_delete, name='day_delete'),

    # FlightMaster URLs
    path('flights/', views.flight_list, name='flight_list'),
    path('flights/create/', views.flight_create, name='flight_create'),
    path('flights/<int:pk>/update/', views.flight_update, name='flight_update'),
    path('flights/<int:pk>/delete/', views.flight_delete, name='flight_delete'),

    # FlightFareMap URLs
    path('flight_fares/', views.flight_fare_map_list, name='flight_fare_map_list'),
    path('flight_fares/create/', views.flight_fare_map_create, name='flight_fare_map_create'),
    path('flight_fares/<int:pk>/update/', views.flight_fare_map_update, name='flight_fare_map_update'),
    path('flight_fares/<int:pk>/delete/', views.flight_fare_map_delete, name='flight_fare_map_delete'),

    path('search_flights/', views.search_flights, name='search_flights'),
    path('flight/<int:flight_id>/availability/', views.check_availability, name='check_availability'),
    path('book_ticket/<str:flight_no>/<int:flight_class_id>/', views.book_ticket, name='book_ticket'),
    path('payment/<str:short_token>/', views.payment, name='payment'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('booking_confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('cancel-ticket/<str:pnr_number>/', views.cancel_ticket, name='cancel_ticket'),
    

    # FlightDayMap URLs
    path('flight_days/', views.flight_day_map_list, name='flight_day_map_list'),
    path('flight_days/create/', views.flight_day_map_create, name='flight_day_map_create'),
    path('flight_days/<int:pk>/update/', views.flight_day_map_update, name='flight_day_map_update'),
    path('flight_days/<int:pk>/delete/', views.flight_day_map_delete, name='flight_day_map_delete'),

    # CustomerDetails URLs
    path('customers/', views.customer_details_list, name='customer_details_list'),
    path('customers/create/', views.customer_details_create, name='customer_details_create'),
    path('customers/<int:pk>/update/', views.customer_details_update, name='customer_details_update'),
    path('customers/<int:pk>/delete/', views.customer_details_delete, name='customer_details_delete'),

    path('reservation/', views.reservation, name='reservation'),
]