import googlemaps
from django.conf import settings
from .models import Ride, Location
from users.models import Driver

class GoogleMapsService:
    def __init__(self):
        self.client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY) if settings.GOOGLE_MAPS_API_KEY else None
    
    def geocode_postcode(self, postcode):
        if not self.client:
            # Fallback coordinates for London if no API key
            return 51.5074, -0.1278
        try:
            result = self.client.geocode(postcode)
            if result:
                location = result[0]['geometry']['location']
                return location['lat'], location['lng']
        except:
            pass
        return 51.5074, -0.1278  # Default to London
    
    def calculate_distance(self, pickup_location, dropoff_location):
        if not self.client:
            return 5.0  # Default distance
        try:
            result = self.client.distance_matrix(
                origins=[(pickup_location.latitude, pickup_location.longitude)],
                destinations=[(dropoff_location.latitude, dropoff_location.longitude)],
                units="metric"
            )
            distance = result['rows'][0]['elements'][0]['distance']['value'] / 1000  # Convert to km
            return distance
        except:
            return 5.0

class FareCalculationStrategy:
    def calculate_fare(self, distance, ride_type, surge_multiplier=1.0):
        base_rates = {
            'STANDARD': 2.0,
            'POOL': 1.5,
            'LUXURY': 3.5
        }
        base_fare = 5.0
        rate_per_km = base_rates.get(ride_type, 2.0)
        return (base_fare + (distance * rate_per_km)) * surge_multiplier

class RideManagementSystem:
    def __init__(self):
        self.maps_service = GoogleMapsService()
        self.fare_calculator = FareCalculationStrategy()
    
    def find_nearby_drivers(self, pickup_location, radius_km=10):
        # Simple implementation - in production, use spatial queries
        return Driver.objects.filter(is_available=True)[:5]
    
    def create_ride(self, passenger, ride_data):
        # Geocode postcodes to get coordinates
        pickup_lat, pickup_lng = self.maps_service.geocode_postcode(ride_data['pickup_postcode'])
        dropoff_lat, dropoff_lng = self.maps_service.geocode_postcode(ride_data['dropoff_postcode'])
        
        pickup_location = Location.objects.create(
            latitude=pickup_lat,
            longitude=pickup_lng,
            address=ride_data['pickup_address'],
            postcode=ride_data['pickup_postcode']
        )
        
        dropoff_location = Location.objects.create(
            latitude=dropoff_lat,
            longitude=dropoff_lng,
            address=ride_data['dropoff_address'],
            postcode=ride_data['dropoff_postcode']
        )
        
        distance = self.maps_service.calculate_distance(pickup_location, dropoff_location)
        fare = self.fare_calculator.calculate_fare(distance, ride_data['ride_type'])
        
        print(f"Distance: {distance}km, Ride Type: {ride_data['ride_type']}, Fare: £{fare}")
        
        ride = Ride.objects.create(
            passenger=passenger,
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            ride_type=ride_data['ride_type'],
            distance=distance,
            fare=fare,
            payment_method=ride_data.get('payment_method', 'WALLET')
        )
        
        return ride