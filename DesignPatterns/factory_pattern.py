"""
    FACTORY DESIGN PATTERN

The factory method design pattern is a creational pattern that addresses object creation without specifying concrete classes. 
It defines an interface for object creation, letting subclasses decide which class to instantiate. 
Instead of direct instantiation, the process is delegated to a factory method within an abstract creator. 
Concrete subclasses implement this method to produce specific product instances. This pattern is useful when object types may 
vary or are determined at runtime.
Please note that using a abstract factory class is not always used/required

"""


from abc import ABC, abstractmethod

# 1. Product Interface/Abstract Class
class Vehicle(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

# 2. Concrete Products
class Car(Vehicle):
    def start(self):
        print("Car engine starting...")

    def stop(self):
        print("Car engine stopping.")

class Motorcycle(Vehicle):
    def start(self):
        print("Motorcycle starting with a kick...")

    def stop(self):
        print("Motorcycle engine shutting down.")

# 3. Creator Abstract Class
class VehicleFactory(ABC):
    @abstractmethod
    def create_vehicle(self) -> Vehicle:
        pass

    def some_operation(self):  # Other methods can exist in the creator
        vehicle = self.create_vehicle()
        vehicle.start()
        vehicle.stop()

# 4. Concrete Creators
class CarFactory(VehicleFactory):
    def create_vehicle(self) -> Vehicle:
        return Car()

class MotorcycleFactory(VehicleFactory):
    def create_vehicle(self) -> Vehicle:
        return Motorcycle()

# Client Code
if __name__ == "__main__":
    car_factory = CarFactory()
    car_factory.some_operation() # Output: Car engine starting... \n Car engine stopping.

    motorcycle_factory = MotorcycleFactory()
    motorcycle_factory.some_operation() # Output: Motorcycle starting with a kick... \n Motorcycle engine shutting down.
