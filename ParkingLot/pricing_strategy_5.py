"""
Spot Type	Rate (₹/hour)
Handicapped	10
Compact	20
Large	30
Truck	50

"""
from abc import ABC, abstractmethod


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, hours: int) -> float:
        pass


class HandicappedPricing(PricingStrategy):
    def calculate_price(self, hours: int) -> float:
        return hours * 10
    
class CompactPricing(PricingStrategy):
    def calculate_price(self, hours: int) -> float:
        return hours * 20
    
class LargePricing(PricingStrategy):
    def calculate_price(self, hours: int) -> float:
        return hours * 30
    
class TruckPricing(PricingStrategy):
    def calculate_price(self, hours: int) -> float:
        return hours * 50
    

class PricingStrategyFactory:
    @staticmethod
    def get_strategy(spot_type: str) -> PricingStrategy:
        if spot_type == 'Handicapped':
            return HandicappedPricing()
        elif spot_type == "Compact":
            return CompactPricing()
        elif spot_type == "Large":
            return LargePricing()
        elif spot_type == "Truck":
            return TruckPricing()
        else:
            raise Exception(f"No pricing strategy found for type: {spot_type}")