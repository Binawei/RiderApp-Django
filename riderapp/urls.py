from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/rides/', include('rides.urls')),
    path('api/payments/', include('payments.urls')),
    path('actuator/health/', lambda request: HttpResponse('{"status":"UP"}', content_type='application/json')),
]