from django.contrib import admin
from .models import User, Driver, Passenger

admin.site.register(User)
admin.site.register(Driver)
admin.site.register(Passenger)