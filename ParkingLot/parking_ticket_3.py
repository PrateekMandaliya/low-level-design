import uuid
from datetime import datetime

class ParkingTicket:
    def __init__(self, spot, gate_id):
        self.ticket_id = str(uuid.uuid4())
        self.parking_spot_id = spot.spot_id
        self.parking_spot_type = spot.get_type()
        self.gate_id = gate_id
        self.issue_time = datetime.now()
        self.exit_time = None
        self.paid = False
        self.amount = 0.0

    
    def mark_exit(self, exit_time):
        self.exit_time = exit_time
        

    def mark_paid(self, amount):
        self.paid = True
        self.amount = amount

    
    def __repr__(self):
        return f"Ticket({self.ticket_id}, Spot: {self.parking_spot_id}, Type: {self.parking_spot_type}, Entry: {self.issue_time})"
