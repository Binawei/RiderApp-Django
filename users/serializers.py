from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Driver, Passenger

class UserResponseSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()
    passenger_id = serializers.SerializerMethodField()
    driver_id = serializers.SerializerMethodField()
    wallet_balance = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'user_type', 'passenger_id', 'driver_id', 'wallet_balance']
    
    def get_user_type(self, obj):
        if hasattr(obj, 'driver'):
            return 'driver'
        elif hasattr(obj, 'passenger'):
            return 'passenger'
        return None
    
    def get_passenger_id(self, obj):
        return obj.passenger.id if hasattr(obj, 'passenger') else None
    
    def get_driver_id(self, obj):
        return obj.driver.id if hasattr(obj, 'driver') else None
    
    def get_wallet_balance(self, obj):
        if hasattr(obj, 'passenger'):
            return float(obj.passenger.wallet_balance)
        return 0.0

class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class DriverRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    firstName = serializers.CharField(source='first_name', write_only=True)
    lastName = serializers.CharField(source='last_name', write_only=True)
    vehicleNumber = serializers.CharField(source='license_plate')
    vehicleType = serializers.CharField(source='vehicle_make')
    
    class Meta:
        model = User
        fields = ['email', 'password', 'firstName', 'lastName', 'phone', 
                 'vehicleNumber', 'vehicleType']
    
    def create(self, validated_data):
        driver_data = {
            'license_plate': validated_data.pop('license_plate'),
            'vehicle_make': validated_data.pop('vehicle_make'),
            'vehicle_model': 'Standard',
            'vehicle_year': 2020,
            'vehicle_color': 'Black',
            'license_number': validated_data.get('license_plate', 'DEFAULT'),
        }
        
        user = User.objects.create_user(
            username=validated_data['email'],
            **validated_data
        )
        Driver.objects.create(user=user, **driver_data)
        return user

class PassengerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    firstName = serializers.CharField(source='first_name', write_only=True)
    lastName = serializers.CharField(source='last_name', write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'firstName', 'lastName', 'phone']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            **validated_data
        )
        Passenger.objects.create(user=user)
        return user

class ForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordRequestSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()