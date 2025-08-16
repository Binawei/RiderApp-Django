# RiderApp Django

A Django REST API version of the RiderApp ride-sharing platform with all the same features as the Spring Boot version.

## Features

- User registration and authentication (Drivers and Passengers)
- JWT token-based authentication
- Ride request and management system
- Payment processing with Stripe integration
- Google Maps integration for distance calculation
- Multiple fare calculation strategies (Standard, Pool, Luxury)
- Real-time ride status updates

## API Endpoints

### User Management
- `POST /api/users/register/driver/` - Register as driver
- `POST /api/users/register/passenger/` - Register as passenger  
- `POST /api/users/login/` - User login
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/update/` - Update user profile
- `POST /api/users/forgot-password/` - Request password reset
- `POST /api/users/reset-password/` - Reset password

### Ride Management
- `POST /api/rides/request/` - Request a ride
- `GET /api/rides/history/` - Get ride history
- `GET /api/rides/current/` - Get current active ride
- `POST /api/rides/<id>/accept/` - Accept ride (driver)
- `POST /api/rides/<id>/start/` - Start ride (driver)
- `POST /api/rides/<id>/complete/` - Complete ride (driver)
- `POST /api/rides/<id>/cancel/` - Cancel ride
- `GET /api/rides/available/` - Get available rides (driver)

### Payment Processing
- `POST /api/payments/process/` - Process payment
- `GET /api/payments/history/` - Get payment history
- `GET /api/payments/<id>/status/` - Get payment status

### Health Check
- `GET /actuator/health/` - Application health status

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
SECRET_KEY=your-secret-key
DB_NAME=Rider
DB_USER=postgres
DB_PASSWORD=your-password
SECRET=stripe-secret-key
PUBLISH=stripe-publishable-key
MAP=google-maps-api-key
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run the server:
```bash
python manage.py runserver 8000
```

## Docker

Build and run with Docker:
```bash
docker build -t riderapp-django .
docker run -p 8000:8000 riderapp-django
```

## Architecture

The Django version maintains the same architectural patterns as the Spring Boot version:

- **Strategy Pattern**: Multiple fare calculation strategies
- **Factory Pattern**: Payment processing factory
- **Observer Pattern**: Ride status notifications (can be extended)
- **Service Layer**: Business logic separation
- **Repository Pattern**: Django ORM as data access layer

## Models

- **User**: Custom user model extending AbstractUser
- **Driver**: Driver-specific information and vehicle details
- **Passenger**: Passenger-specific information
- **Ride**: Ride information with pickup/dropoff locations
- **Location**: Geographic location data
- **Payment**: Payment processing and status tracking