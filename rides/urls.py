from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.request_ride, name='request_ride'),
    path('history/', views.get_ride_history, name='get_ride_history'),
    path('current/', views.get_current_ride, name='get_current_ride'),
    path('<int:ride_id>/accept/', views.accept_ride, name='accept_ride'),
    path('<int:ride_id>/start/', views.start_ride, name='start_ride'),
    path('<int:ride_id>/complete/', views.complete_ride, name='complete_ride'),
    path('<int:ride_id>/cancel/', views.cancel_ride, name='cancel_ride'),
    path('<int:ride_id>/rate/', views.rate_ride, name='rate_ride'),
    path('available/', views.get_available_rides, name='get_available_rides'),
]