from abc import ABC, abstractmethod
import uuid

class ParkingSpot(ABC):
    def __init__(self, spot_id=None):
        self.spot_id = spot_id or uuid.uuid4()
        self.is_reserved = False
    
    @abstractmethod
    def get_type(self):
        pass

    def reserve(self):
        if self.is_reserved:
            raise Exception(f'Spot {self.spot_id} is already reserved.')
        self.is_reserved = True
        return True
    
    def release(self):
        self.is_reserved = False


class HandicappedSpot(ParkingSpot):
    def get_type(self):
        return "Handicapped"
    

class CompactSpot(ParkingSpot):
    def get_type(self):
        return "Compact"


class LargeSpot(ParkingSpot):
    def get_type(self):
        return "Large"
    

class TruckSpot(ParkingSpot):
    def get_type(self):
        return "TruckSpot"