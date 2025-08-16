from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    vehicle_make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_year = models.IntegerField()
    vehicle_color = models.CharField(max_length=30)
    license_plate = models.CharField(max_length=20)
    is_available = models.BooleanField(default=True)
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)
    rating = models.FloatField(default=5.0)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"Driver: {self.user.get_full_name()}"

class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_payment_method = models.CharField(max_length=20, default='card')
    rating = models.FloatField(default=5.0)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"Passenger: {self.user.get_full_name()}"