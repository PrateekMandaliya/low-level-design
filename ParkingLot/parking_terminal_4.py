from abc import ABC, abstractmethod
from ParkingLot.parking_lot_manager_2 import ParkingLotManager
from ParkingLot.parking_ticket_3 import ParkingTicket
from ParkingLot.pricing_strategy_5 import PricingStrategyFactory


class Terminal(ABC):
    def __init__(self, terminal_id, gate_id):
        self.terminal_id = terminal_id
        self.gate_id = gate_id
    

class EntryTerminal(Terminal):
    def get_ticket(self, spot_type):
        # To create ticket I need spot, gate_id
        manager = ParkingLotManager.get_instance()
        spot = manager.get_nearest_available_spot(self.gate_id, spot_type)

        if not spot:
            print(f"No available {spot_type} spots at gate {self.gate_id}")
            return None
        
        ticket = ParkingTicket(spot, self.gate_id)
        print(f"Issued ticket {ticket}")
        return ticket
    

from datetime import datetime

class ExitTerminal(Terminal):
    def accept_ticket(self, ticket: ParkingTicket):
        if ticket.paid:
            print("Ticket already paid")
            return
        
        # Calculate parking fare
        exit_time = datetime.now()
        ticket.mark_exit(exit_time)

        duration_hours = max(1, (exit_time - ticket.issue_time).seconds // 3600)
        # rate_per_hour = 20
        # amount = duration_hours * rate_per_hour

        strategy = PricingStrategyFactory.get_strategy(ticket.parking_spot_type)
        amount = strategy.calculate_price(duration_hours)

        print(f"Total due: ₹{amount} for {duration_hours} hour(s)")
        ticket.mark_paid(amount)

        # Release the parking spot
        manager = ParkingLotManager.get_instance()
        manager.release_parking_spot(ticket.parking_spot_id)
        # Need to find and release spot — assuming we maintain spot_id→spot_map

        print(f"Payment successful for Ticket {ticket.ticket_id}. Spot is now free.")

