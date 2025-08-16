from django.db import models
from users.models import Driver, Passenger

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=20)

class Ride(models.Model):
    class RideStatus(models.TextChoices):
        REQUESTED = 'REQUESTED', 'Requested'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        PICKED_UP = 'PICKED_UP', 'Picked Up'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    class RideType(models.TextChoices):
        STANDARD = 'STANDARD', 'Standard'
        POOL = 'POOL', 'Pool'
        LUXURY = 'LUXURY', 'Luxury'
    
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pickup_rides')
    dropoff_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='dropoff_rides')
    request_time = models.DateTimeField(auto_now_add=True)
    pickup_time = models.DateTimeField(null=True, blank=True)
    dropoff_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=RideStatus.choices, default=RideStatus.REQUESTED)
    ride_type = models.CharField(max_length=20, choices=RideType.choices, default=RideType.STANDARD)
    fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    distance = models.FloatField(default=0)
    rating = models.IntegerField(null=True, blank=True)
    surge_multiplier = models.FloatField(default=1.0)
    payment_method = models.CharField(max_length=50, default='card')
    
    def __str__(self):
        return f"Ride {self.id} - {self.status}"