from django.contrib import admin
from .models import (
    ClassMaster, CompanyMaster, AerodrumMaster, DayMaster, FlightMaster,
    FlightFareMap, FlightDayMap, CustomerDetails
)

@admin.register(ClassMaster)
class ClassMasterAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'class_name')
    search_fields = ('class_name',)

@admin.register(CompanyMaster)
class CompanyMasterAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'company_name')
    search_fields = ('company_name',)

@admin.register(AerodrumMaster)
class AerodrumMasterAdmin(admin.ModelAdmin):
    list_display = ('aerodrum_id', 'aerodrum_name', 'city', 'state')
    search_fields = ('aerodrum_name', 'city', 'state')

@admin.register(DayMaster)
class DayMasterAdmin(admin.ModelAdmin):
    list_display = ('day_id', 'day_name')
    search_fields = ('day_name',)

@admin.register(FlightMaster)
class FlightMasterAdmin(admin.ModelAdmin):
    list_display = (
        'flight_no', 'flight_name', 'company', 'source', 'destination',
        'departure_time', 'arrival_time'
    )
    search_fields = ('flight_name', 'company__company_name', 'source__aerodrum_name', 'destination__aerodrum_name')
    list_filter = ('company', 'source', 'destination')

@admin.register(FlightFareMap)
class FlightFareMapAdmin(admin.ModelAdmin):
    list_display = ('ff_id', 'flight', 'flight_class', 'no_of_seats', 'fare')
    search_fields = ('flight__flight_name', 'flight_class__class_name')
    list_filter = ('flight', 'flight_class')

@admin.register(FlightDayMap)
class FlightDayMapAdmin(admin.ModelAdmin):
    list_display = ('fd_id', 'flight', 'day')
    search_fields = ('flight__flight_name', 'day__day_name')


@admin.register(CustomerDetails)
class CustomerDetailsAdmin(admin.ModelAdmin):
    list_display = (
       'passport_id', 'customer_name', 'age', 'gender',
        'city', 'email_id', 'contact_no',  'booking_date',
        'flight_class', 'flight'
    )
    search_fields = ('customer_name', 'passport_id', 'email_id', 'contact_no', 'flight__flight_name')
    list_filter = ('flight_class', 'flight')
