import stripe
from django.conf import settings
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentStrategy:
    def process_payment(self, payment, **kwargs):
        raise NotImplementedError

class CreditCardPayment(PaymentStrategy):
    def process_payment(self, payment, stripe_token=None):
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(payment.amount * 100),  # Convert to cents
                currency='usd',
                payment_method_types=['card'],
                metadata={'ride_id': payment.ride.id}
            )
            payment.stripe_payment_intent_id = intent.id
            payment.status = Payment.PaymentStatus.COMPLETED
            payment.save()
            return True
        except stripe.error.StripeError:
            payment.status = Payment.PaymentStatus.FAILED
            payment.save()
            return False

class WalletPayment(PaymentStrategy):
    def process_payment(self, payment, **kwargs):
        # Simulate wallet payment processing
        payment.status = Payment.PaymentStatus.COMPLETED
        payment.save()
        return True

class PaymentFactory:
    @staticmethod
    def get_payment_strategy(payment_type):
        strategies = {
            Payment.PaymentType.CREDIT_CARD: CreditCardPayment(),
            Payment.PaymentType.WALLET: WalletPayment(),
        }
        return strategies.get(payment_type)

class StripeService:
    def __init__(self):
        self.payment_factory = PaymentFactory()
    
    def process_payment(self, payment, **kwargs):
        strategy = self.payment_factory.get_payment_strategy(payment.payment_type)
        if strategy:
            return strategy.process_payment(payment, **kwargs)
        return False