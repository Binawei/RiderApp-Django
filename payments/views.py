from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentRequestSerializer, PaymentResponseSerializer
from .services import StripeService
from rides.models import Ride

stripe_service = StripeService()

@api_view(['POST'])
def process_payment(request):
    serializer = PaymentRequestSerializer(data=request.data)
    if serializer.is_valid():
        try:
            ride = Ride.objects.get(id=serializer.validated_data['ride_id'])
            
            # Check if user is authorized for this ride
            if ride.passenger.user != request.user:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
            
            payment = Payment.objects.create(
                ride=ride,
                amount=ride.fare,
                payment_type=serializer.validated_data['payment_type']
            )
            
            success = stripe_service.process_payment(
                payment, 
                stripe_token=serializer.validated_data.get('stripe_token')
            )
            
            if success:
                return Response(PaymentResponseSerializer(payment).data)
            else:
                return Response({'error': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)
                
        except Ride.DoesNotExist:
            return Response({'error': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_payment_history(request):
    # Get payments for rides where user is the passenger
    payments = Payment.objects.filter(ride__passenger__user=request.user).order_by('-created_at')
    return Response(PaymentResponseSerializer(payments, many=True).data)

@api_view(['GET'])
def get_payment_status(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id, ride__passenger__user=request.user)
        return Response(PaymentResponseSerializer(payment).data)
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)