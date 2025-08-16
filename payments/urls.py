from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.process_payment, name='process_payment'),
    path('history/', views.get_payment_history, name='get_payment_history'),
    path('<int:payment_id>/status/', views.get_payment_status, name='get_payment_status'),
]