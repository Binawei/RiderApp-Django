from rest_framework import serializers
from .models import Payment

class PaymentRequestSerializer(serializers.Serializer):
    ride_id = serializers.IntegerField()
    payment_type = serializers.ChoiceField(choices=Payment.PaymentType.choices)
    stripe_token = serializers.CharField(required=False)

class PaymentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'ride', 'amount', 'payment_type', 'status', 
                 'stripe_payment_intent_id', 'created_at', 'updated_at']