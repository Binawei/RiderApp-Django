from abc import ABC, abstractmethod

class RideObserver(ABC):
    @abstractmethod
    def update(self, ride, event_type):
        pass

class DriverNotificationObserver(RideObserver):
    def update(self, ride, event_type):
        if event_type == 'RIDE_REQUESTED':
            # Notify nearby drivers
            print(f"Notifying drivers about new ride request: {ride.id}")
        elif event_type == 'RIDE_ACCEPTED':
            # Notify passenger that driver accepted
            print(f"Driver {ride.driver.user.first_name} accepted ride {ride.id}")

class PassengerNotificationObserver(RideObserver):
    def update(self, ride, event_type):
        if event_type == 'DRIVER_ARRIVED':
            print(f"Driver has arrived for ride {ride.id}")
        elif event_type == 'RIDE_STARTED':
            print(f"Ride {ride.id} has started")

class RideSubject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self, ride, event_type):
        for observer in self._observers:
            observer.update(ride, event_type)