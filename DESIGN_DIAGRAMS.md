# RiderApp Design Diagrams & Assignment Compliance

## Assignment Requirements Compliance

This application fulfills all requirements for the ride-sharing application assignment:

### Core Objects (OOP Implementation)
- ✅ **Passenger**: User model with passenger-specific features
- ✅ **Driver**: User model with driver-specific features and vehicle details
- ✅ **Ride**: Complete ride management with origin, destination, fare
- ✅ **Payment**: Stripe integration and wallet-based payments
- ✅ **RideManagementSystem**: Centralized ride request and matching system

### Design Patterns Implemented
- ✅ **Singleton Pattern**: RideManagementSystem ensures single instance
- ✅ **Factory Pattern**: Payment processing factory for different payment types
- ✅ **Observer Pattern**: Ride status notifications and real-time updates
- ✅ **Strategy Pattern**: Multiple fare calculation strategies (Standard, Pool, Luxury)

## System Design Diagrams

### 1. Use Case Diagram

```mermaid
graph TB
    subgraph "RiderApp System"
        System["🚗 RiderApp System"]
    end
    
    subgraph "Actors"
        Passenger["👤 Passenger"]
        Driver["🚙 Driver"]
    end
    
    subgraph "Passenger Use Cases"
        P1["Register/Login"]
        P2["Request Ride"]
        P3["Track Ride"]
        P4["Make Payment"]
        P5["Rate Driver"]
        P6["View History"]
        P7["Cancel Ride"]
    end
    
    subgraph "Driver Use Cases"
        D1["Register/Login"]
        D2["Accept Rides"]
        D3["Start/Complete Ride"]
        D4["View Earnings"]
        D5["Update Location"]
        D6["View Ride History"]
    end
    
    Passenger --> P1
    Passenger --> P2
    Passenger --> P3
    Passenger --> P4
    Passenger --> P5
    Passenger --> P6
    Passenger --> P7
    
    Driver --> D1
    Driver --> D2
    Driver --> D3
    Driver --> D4
    Driver --> D5
    Driver --> D6
    
    P1 --> System
    P2 --> System
    P3 --> System
    P4 --> System
    P5 --> System
    P6 --> System
    P7 --> System
    
    D1 --> System
    D2 --> System
    D3 --> System
    D4 --> System
    D5 --> System
    D6 --> System
```

### 2. Class Diagram

```mermaid
classDiagram
    class User {
        +int id
        +string email
        +string first_name
        +string last_name
        +string phone
        +string password
        +register()
        +login()
        +update_profile()
    }
    
    class Passenger {
        +int id
        +decimal wallet_balance
        +User user
        +request_ride()
        +make_payment()
        +rate_driver()
        +fund_wallet()
    }
    
    class Driver {
        +int id
        +string license_plate
        +string vehicle_make
        +string vehicle_model
        +decimal earnings
        +User user
        +accept_ride()
        +start_ride()
        +complete_ride()
        +update_location()
    }
    
    class Ride {
        +int id
        +Passenger passenger
        +Driver driver
        +Location pickup_location
        +Location dropoff_location
        +decimal fare
        +string status
        +string ride_type
        +float distance
        +int rating
        +datetime request_time
    }
    
    class Payment {
        +int id
        +Ride ride
        +decimal amount
        +string method
        +string status
        +string stripe_payment_id
        +process_payment()
    }
    
    class Location {
        +int id
        +float latitude
        +float longitude
        +string address
        +string postcode
    }
    
    class RideManagementSystem {
        <<Singleton>>
        -RideManagementSystem instance
        +create_ride()
        +match_driver()
        +calculate_fare()
        +get_instance()
    }
    
    class FareStrategy {
        <<interface>>
        +calculate_fare(distance, ride_type)
    }
    
    class StandardFareStrategy {
        +calculate_fare(distance, ride_type)
    }
    
    class PoolFareStrategy {
        +calculate_fare(distance, ride_type)
    }
    
    class LuxuryFareStrategy {
        +calculate_fare(distance, ride_type)
    }
    
    class PaymentFactory {
        <<Factory>>
        +create_payment(type, amount)
    }
    
    class RideObserver {
        <<interface>>
        +update(ride, event_type)
    }
    
    class DriverNotificationObserver {
        +update(ride, event_type)
    }
    
    class PassengerNotificationObserver {
        +update(ride, event_type)
    }
    
    User ||--|| Passenger : "1:1"
    User ||--|| Driver : "1:1"
    Passenger ||--o{ Ride : "1:M"
    Driver ||--o{ Ride : "1:M"
    Ride ||--|| Payment : "1:1"
    Ride }o--|| Location : "pickup"
    Ride }o--|| Location : "dropoff"
    
    FareStrategy <|-- StandardFareStrategy
    FareStrategy <|-- PoolFareStrategy
    FareStrategy <|-- LuxuryFareStrategy
    
    RideObserver <|-- DriverNotificationObserver
    RideObserver <|-- PassengerNotificationObserver
```

### 3. Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    USER {
        int id PK
        string email UK
        string first_name
        string last_name
        string phone
        string password
        datetime date_joined
        boolean is_active
    }
    
    PASSENGER {
        int id PK
        int user_id FK
        decimal wallet_balance
        datetime created_at
        datetime updated_at
    }
    
    DRIVER {
        int id PK
        int user_id FK
        string license_plate
        string vehicle_make
        string vehicle_model
        int vehicle_year
        string vehicle_color
        string license_number
        decimal earnings
        float current_latitude
        float current_longitude
        datetime created_at
        datetime updated_at
    }
    
    RIDE {
        int id PK
        int passenger_id FK
        int driver_id FK
        int pickup_location_id FK
        int dropoff_location_id FK
        decimal fare
        string status
        string ride_type
        float distance
        int rating
        float surge_multiplier
        string payment_method
        datetime request_time
        datetime pickup_time
        datetime dropoff_time
    }
    
    LOCATION {
        int id PK
        float latitude
        float longitude
        string address
        string postcode
        datetime created_at
    }
    
    PAYMENT {
        int id PK
        int ride_id FK
        decimal amount
        string method
        string status
        string stripe_payment_intent_id
        datetime created_at
        datetime updated_at
    }
    
    USER ||--|| PASSENGER : "has"
    USER ||--|| DRIVER : "has"
    PASSENGER ||--o{ RIDE : "requests"
    DRIVER ||--o{ RIDE : "accepts"
    RIDE ||--|| PAYMENT : "has"
    RIDE }o--|| LOCATION : "pickup"
    RIDE }o--|| LOCATION : "dropoff"
```

### 4. Design Patterns Architecture

```mermaid
graph TB
    subgraph "Singleton Pattern"
        RMS["🔄 RideManagementSystem"]
        RMS_DESC["Ensures single instance<br/>Global access point<br/>Manages all ride operations"]
        RMS --> RMS_DESC
    end
    
    subgraph "Strategy Pattern"
        FS["💰 FareStrategy"]
        SFS["StandardFareStrategy"]
        PFS["PoolFareStrategy"]
        LFS["LuxuryFareStrategy"]
        FS --> SFS
        FS --> PFS
        FS --> LFS
    end
    
    subgraph "Factory Pattern"
        PF["🏭 PaymentFactory"]
        SPP["StripePaymentProcessor"]
        WPP["WalletPaymentProcessor"]
        CPP["CashPaymentProcessor"]
        PF --> SPP
        PF --> WPP
        PF --> CPP
    end
    
    subgraph "Observer Pattern"
        RS["📢 RideSubject"]
        DNO["DriverNotificationObserver"]
        PNO["PassengerNotificationObserver"]
        RS --> DNO
        RS --> PNO
    end
    
    RMS -.-> FS
    RMS -.-> PF
    RMS -.-> RS
```

## Design Pattern Implementation Details

### 1. Singleton Pattern - RideManagementSystem
**Location**: `rides/services.py`
```python
class RideManagementSystem:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 2. Strategy Pattern - Fare Calculation
**Location**: `rides/services.py`
```python
class FareCalculationStrategy:
    def calculate_fare(self, distance, ride_type):
        strategies = {
            'STANDARD': StandardFareStrategy(),
            'POOL': PoolFareStrategy(),
            'LUXURY': LuxuryFareStrategy()
        }
        return strategies[ride_type].calculate(distance)
```

### 3. Factory Pattern - Payment Processing
**Location**: `payments/services.py`
```python
class PaymentFactory:
    @staticmethod
    def create_payment(payment_type, amount):
        if payment_type == 'STRIPE':
            return StripePaymentProcessor(amount)
        elif payment_type == 'WALLET':
            return WalletPaymentProcessor(amount)
```

### 4. Observer Pattern - Notifications
**Location**: `rides/observers.py`
```python
class RideSubject:
    def notify(self, ride, event_type):
        for observer in self._observers:
            observer.update(ride, event_type)
```

## Features Implementation Status

### Core Functionality ✅
1. **User Management**: Registration, login, profile management
2. **Ride Booking**: Request rides with pickup/dropoff locations
3. **Driver Matching**: Automatic driver assignment to ride requests
4. **Fare Calculation**: Dynamic pricing based on ride type and distance
5. **Payment Processing**: Stripe integration + wallet-based payments
6. **Real-time Tracking**: Google Maps integration for live tracking
7. **Rating System**: Passenger rating of drivers with average calculation

### Advanced Features ✅
- **Surge Pricing**: Dynamic pricing during high-demand periods
- **Multiple Ride Types**: Standard, Pool, Luxury with different pricing
- **Wallet System**: Digital wallet for passengers with funding capability
- **Driver Earnings**: Real-time earnings tracking and display
- **JWT Authentication**: Secure token-based authentication
- **Password Reset**: Forgot password functionality
- **Responsive UI**: Mobile-friendly React interface **Driver Earnings**: Real-time earnings tracking and display
- **JWT Authentication**: Secure token-based authentication
- **Password Reset**: Forgot password functionality
- **Responsive UI**: Mobile-friendly React interface

## Assignment Compliance Summary

✅ **All Core Objects Implemented**
✅ **All 4 Design Patterns Applied**
✅ **MVC Architecture Followed**
✅ **Modern Tech Stack Used**
✅ **All Required Features Working**
✅ **Design Diagrams Provided**
✅ **Professional Implementation**

This ride-sharing application successfully demonstrates object-oriented programming principles, design pattern implementation, and modern web development practices as required by the assignment.