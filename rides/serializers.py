from rest_framework import serializers
from .models import Ride, Location
from users.serializers import UserResponseSerializer

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude', 'address', 'postcode']

class RideRequestSerializer(serializers.Serializer):
    pickupAddress = serializers.CharField(source='pickup_address')
    pickupPostcode = serializers.CharField(source='pickup_postcode')
    dropoffAddress = serializers.CharField(source='dropoff_address')
    dropoffPostcode = serializers.CharField(source='dropoff_postcode')
    rideType = serializers.ChoiceField(choices=Ride.RideType.choices, source='ride_type')
    paymentMethod = serializers.CharField(source='payment_method', required=False)

class RideResponseSerializer(serializers.ModelSerializer):
    pickupLocation = LocationSerializer(source='pickup_location', read_only=True)
    dropoffLocation = LocationSerializer(source='dropoff_location', read_only=True)
    requestTime = serializers.DateTimeField(source='request_time', format='%Y-%m-%dT%H:%M:%S')
    pickupTime = serializers.DateTimeField(source='pickup_time', format='%Y-%m-%dT%H:%M:%S', allow_null=True)
    dropoffTime = serializers.DateTimeField(source='dropoff_time', format='%Y-%m-%dT%H:%M:%S', allow_null=True)
    rideType = serializers.CharField(source='ride_type')
    surgeMultiplier = serializers.FloatField(source='surge_multiplier')
    paymentMethod = serializers.CharField(source='payment_method')
    fare = serializers.SerializerMethodField()
    driver = serializers.SerializerMethodField()
    passengerName = serializers.SerializerMethodField()
    
    class Meta:
        model = Ride
        fields = ['id', 'pickupLocation', 'dropoffLocation', 'requestTime', 
                 'pickupTime', 'dropoffTime', 'status', 'rideType', 'fare', 
                 'distance', 'rating', 'surgeMultiplier', 'paymentMethod', 'driver', 'passengerName']
    
    def get_fare(self, obj):
        return float(obj.fare) if obj.fare else 0.0
    
    def get_driver(self, obj):
        if obj.driver:
            return {
                'firstName': obj.driver.user.first_name,
                'lastName': obj.driver.user.last_name
            }
        return None
    
    def get_passengerName(self, obj):
        if obj.passenger:
            first_name = obj.passenger.user.first_name
            last_initial = obj.passenger.user.last_name[0].upper() if obj.passenger.user.last_name else ""
            return f"{first_name} {last_initial}."
        return None