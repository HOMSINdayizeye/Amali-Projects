from abc import ABC, abstractmethod



class Vehicle(ABC):
    def __init__(self, vehicle_id, make, model, year, rental_rate):
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
        self.rental_rate = rental_rate

    @abstractmethod
    def get_vehicle_type(self):
        pass

    def __str__(self):
        return f"{self.year} {self.make} {self.model} (ID: {self.vehicle_id}) - Rate: ${self.rental_rate}/day"
class Car(Vehicle):
    def __init__(self, vehicle_id, make, model, year, rental_rate, num_doors):
        super().__init__(vehicle_id, make, model, year, rental_rate)
        self.num_doors = num_doors

    def get_vehicle_type(self):
        return "Car"

    def __str__(self):
        return f"{super().__str__()} - Doors: {self.num_doors}"
    
class Truck(Vehicle):
    def __init__(self, vehicle_id, make, model, year, rental_rate, payload_capacity):
        super().__init__(vehicle_id, make, model, year, rental_rate)
        self.payload_capacity = payload_capacity

    def get_vehicle_type(self):
        return "Truck"

    def __str__(self):
        return f"{super().__str__()} - Payload Capacity: {self.payload_capacity} lbs"
class Bike(Vehicle):
    def __init__(self, vehicle_id, make, model, year, rental_rate, bike_type):
        super().__init__(vehicle_id, make, model, year, rental_rate)
        self.bike_type = bike_type

    def get_vehicle_type(self):
        return "Bike"

    def __str__(self):
        return f"{super().__str__()} - Type: {self.bike_type}"