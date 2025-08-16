from django.urls import path
from . import views

urlpatterns = [
    path('register/driver/', views.register_driver, name='register_driver'),
    path('register/passenger/', views.register_passenger, name='register_passenger'),
    path('login/', views.login, name='login'),
    path('profile/', views.get_profile, name='get_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('passengers/<int:passenger_id>/wallet-balance/', views.get_wallet_balance, name='get_wallet_balance'),
    path('passengers/<int:passenger_id>/fund-wallet/', views.fund_wallet, name='fund_wallet'),
    path('drivers/<int:driver_id>/earnings/', views.get_driver_earnings, name='get_driver_earnings'),
    path('drivers/<int:driver_id>/location/', views.update_driver_location, name='update_driver_location'),
    path('drivers/<int:driver_id>/rating/', views.get_driver_rating, name='get_driver_rating'),
]