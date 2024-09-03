from django.db import models
from accounts.models import Account
import uuid

class ClassMaster(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=30)

    def __str__(self):
        return self.class_name

class CompanyMaster(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=30)

    def __str__(self):
        return self.company_name

class AerodrumMaster(models.Model):
    aerodrum_id = models.AutoField(primary_key=True)
    aerodrum_name = models.CharField(max_length=40)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.aerodrum_name}, {self.city}"

class DayMaster(models.Model):
    day_id = models.AutoField(primary_key=True)
    day_name = models.CharField(max_length=30)

    def __str__(self):
        return self.day_name

class FlightMaster(models.Model):
    flight_no = models.AutoField(primary_key=True)
    flight_name = models.CharField(max_length=30)
    company = models.ForeignKey(CompanyMaster, on_delete=models.CASCADE)
    source = models.ForeignKey(AerodrumMaster, related_name='source_flights', on_delete=models.CASCADE)
    destination = models.ForeignKey(AerodrumMaster, related_name='destination_flights', on_delete=models.CASCADE)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()

    def __str__(self):
        return self.flight_name

class FlightFareMap(models.Model):
    ff_id = models.AutoField(primary_key=True)
    flight = models.ForeignKey(FlightMaster, on_delete=models.CASCADE)
    flight_class = models.ForeignKey(ClassMaster, on_delete=models.CASCADE)
    no_of_seats = models.IntegerField()
    booked_seats = models.JSONField(default=list)
    fare = models.IntegerField()

    def __str__(self):
        return f"{self.flight} - {self.flight_class}"

class FlightDayMap(models.Model):
    fd_id = models.AutoField(primary_key=True)
    flight = models.ForeignKey(FlightMaster, on_delete=models.CASCADE)
    day = models.ForeignKey(DayMaster, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.flight} on {self.day}"



class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.FloatField()  # Changed to FloatField for numeric operations
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class CustomerDetails(models.Model):
    short_token = models.CharField(max_length=10, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.short_token:
            self.short_token = str(uuid.uuid4().hex[:10])  # Generate a unique short token
        super().save(*args, **kwargs)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    passport_id = models.CharField(max_length=30)
    customer_name = models.CharField(max_length=30)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=30)
    email_id = models.CharField(max_length=30)
    contact_no = models.CharField(max_length=20)
    booking_date = models.DateField()
    flight_class = models.ForeignKey('ClassMaster', on_delete=models.CASCADE)
    flight = models.ForeignKey('FlightMaster', on_delete=models.CASCADE)
    STATUS = (
        ('Cancel', 'Cancel'),
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
    )
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    country = models.CharField(max_length=50)
    fare_total = models.FloatField()
    total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    is_reserved = models.BooleanField(default=False)
    pnr_number = models.CharField(max_length=20, unique=True, default='')
    seat_number = models.CharField(max_length=10)
