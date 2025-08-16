from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Driver, Passenger
from .serializers import *

@api_view(['POST'])
@permission_classes([AllowAny])
def register_driver(request):
    serializer = DriverRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserResponseSerializer(user).data,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_passenger(request):
    serializer = PassengerRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserResponseSerializer(user).data,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserResponseSerializer(user).data,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_profile(request):
    return Response(UserResponseSerializer(request.user).data)

@api_view(['PUT'])
def update_profile(request):
    serializer = UserResponseSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    serializer = ForgotPasswordRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            # Generate a simple reset token (in production, use proper token generation)
            reset_token = f"reset_{user.id}_{user.email}"
            return Response({
                'message': 'Password reset instructions sent',
                'reset_token': reset_token  # In production, send via email
            })
        except User.DoesNotExist:
            return Response({'message': 'Password reset instructions sent'})  # Don't reveal if email exists
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = ResetPasswordRequestSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        # Simple token validation (in production, use proper token validation)
        if token.startswith('reset_'):
            try:
                _, user_id, email = token.split('_', 2)
                user = User.objects.get(id=user_id, email=email)
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successful'})
            except (ValueError, User.DoesNotExist):
                return Response({'error': 'Invalid reset token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid reset token'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_wallet_balance(request, passenger_id):
    try:
        passenger = Passenger.objects.get(id=passenger_id, user=request.user)
        return Response(float(passenger.wallet_balance))
    except Passenger.DoesNotExist:
        return Response({'error': 'Passenger not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def fund_wallet(request, passenger_id):
    from decimal import Decimal
    try:
        passenger = Passenger.objects.get(id=passenger_id, user=request.user)
        amount = Decimal(str(request.GET.get('amount', 0)))
        passenger.wallet_balance += amount
        passenger.save()
        return Response({'balance': float(passenger.wallet_balance), 'message': 'Wallet funded successfully'})
    except Passenger.DoesNotExist:
        return Response({'error': 'Passenger not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_driver_earnings(request, driver_id):
    try:
        # Try to find driver by driver_id first, then by user_id
        try:
            driver = Driver.objects.get(id=driver_id, user=request.user)
        except Driver.DoesNotExist:
            # If not found by driver_id, try finding by user_id (for frontend compatibility)
            driver = Driver.objects.get(user_id=driver_id, user=request.user)
        
        return Response({'earnings': float(driver.earnings)}, status=status.HTTP_200_OK)
    except Driver.DoesNotExist:
        return Response({'error': 'Driver not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_driver_location(request, driver_id):
    try:
        # Try to find driver by driver_id first, then by user_id
        try:
            driver = Driver.objects.get(id=driver_id, user=request.user)
        except Driver.DoesNotExist:
            driver = Driver.objects.get(user_id=driver_id, user=request.user)
        
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        if latitude and longitude:
            driver.current_latitude = latitude
            driver.current_longitude = longitude
            driver.save()
        return Response({'message': 'Location updated successfully'})
    except Driver.DoesNotExist:
        return Response({'error': 'Driver not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_driver_rating(request, driver_id):
    from django.db.models import Avg
    from rides.models import Ride
    try:
        # Try to find driver by driver_id first, then by user_id
        try:
            driver = Driver.objects.get(id=driver_id, user=request.user)
        except Driver.DoesNotExist:
            driver = Driver.objects.get(user_id=driver_id, user=request.user)
        
        # Calculate average rating from completed rides
        avg_rating = Ride.objects.filter(
            driver=driver, 
            status='COMPLETED', 
            rating__isnull=False
        ).aggregate(Avg('rating'))['rating__avg']
        
        return Response({'rating': round(avg_rating, 1) if avg_rating else 0.0})
    except Driver.DoesNotExist:
        return Response({'error': 'Driver not found'}, status=status.HTTP_404_NOT_FOUND)