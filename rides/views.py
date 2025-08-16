from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Ride
from .serializers import RideRequestSerializer, RideResponseSerializer
from .services import RideManagementSystem
from users.models import Passenger, Driver

ride_system = RideManagementSystem()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_ride(request):
    try:
        passenger = Passenger.objects.get(user=request.user)
    except Passenger.DoesNotExist:
        return Response({'error': 'User is not a passenger'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = RideRequestSerializer(data=request.data)
    if serializer.is_valid():
        ride = ride_system.create_ride(passenger, serializer.validated_data)
        return Response(RideResponseSerializer(ride).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ride_history(request):
    try:
        # Try passenger first
        passenger = Passenger.objects.get(user=request.user)
        rides = Ride.objects.filter(passenger=passenger).exclude(status='CANCELLED').order_by('-request_time')
        return Response(RideResponseSerializer(rides, many=True).data)
    except Passenger.DoesNotExist:
        try:
            # Try driver
            driver = Driver.objects.get(user=request.user)
            rides = Ride.objects.filter(driver=driver).exclude(status='CANCELLED').order_by('-request_time')
            return Response(RideResponseSerializer(rides, many=True).data)
        except Driver.DoesNotExist:
            return Response({'error': 'User is neither passenger nor driver'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_ride(request):
    try:
        passenger = Passenger.objects.get(user=request.user)
        ride = Ride.objects.filter(
            passenger=passenger,
            status__in=['REQUESTED', 'ACCEPTED', 'PICKED_UP']
        ).first()
        
        if ride:
            return Response(RideResponseSerializer(ride).data)
        return Response({'message': 'No active ride'}, status=status.HTTP_404_NOT_FOUND)
    except Passenger.DoesNotExist:
        return Response({'error': 'User is not a passenger'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_ride(request, ride_id):
    try:
        driver = Driver.objects.get(user=request.user)
    except Driver.DoesNotExist:
        return Response({'error': 'User is not a driver'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        ride = Ride.objects.get(id=ride_id, status='REQUESTED')
        ride.driver = driver
        ride.status = 'ACCEPTED'
        ride.save()
        return Response(RideResponseSerializer(ride).data)
    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found or already accepted'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_ride(request, ride_id):
    try:
        driver = Driver.objects.get(user=request.user)
        ride = Ride.objects.get(id=ride_id, driver=driver, status='ACCEPTED')
        ride.status = 'PICKED_UP'
        ride.pickup_time = timezone.now()
        ride.save()
        return Response(RideResponseSerializer(ride).data)
    except (Driver.DoesNotExist, Ride.DoesNotExist):
        return Response({'error': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_ride(request, ride_id):
    from decimal import Decimal
    try:
        driver = Driver.objects.get(user=request.user)
        ride = Ride.objects.get(id=ride_id, driver=driver, status='PICKED_UP')
        ride.status = 'COMPLETED'
        ride.dropoff_time = timezone.now()
        
        # Process payment - deduct from passenger wallet and add to driver earnings
        passenger = ride.passenger
        fare = Decimal(str(ride.fare))
        
        if passenger.wallet_balance >= fare:
            passenger.wallet_balance -= fare
            passenger.save()
            
            driver.earnings += fare
            driver.save()
            
        ride.save()
        return Response(RideResponseSerializer(ride).data)
    except (Driver.DoesNotExist, Ride.DoesNotExist):
        return Response({'error': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
        if ride.passenger.user == request.user or (ride.driver and ride.driver.user == request.user):
            ride.status = 'CANCELLED'
            ride.save()
            return Response(RideResponseSerializer(ride).data)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_ride(request, ride_id):
    try:
        passenger = Passenger.objects.get(user=request.user)
        ride = Ride.objects.get(id=ride_id, passenger=passenger, status='COMPLETED')
        rating = int(request.data.get('rating') or request.GET.get('rating', 0))
        
        if 1 <= rating <= 5:
            ride.rating = rating
            ride.save()
            return Response(RideResponseSerializer(ride).data)
        return Response({'error': 'Rating must be between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)
    except (Passenger.DoesNotExist, Ride.DoesNotExist):
        return Response({'error': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_rides(request):
    try:
        driver = Driver.objects.get(user=request.user)
        rides = Ride.objects.filter(status='REQUESTED')
        return Response(RideResponseSerializer(rides, many=True).data)
    except Driver.DoesNotExist:
        return Response({'error': 'User is not a driver'}, status=status.HTTP_400_BAD_REQUEST)