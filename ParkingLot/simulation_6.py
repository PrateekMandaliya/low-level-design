import time
from datetime import timedelta
from ParkingLot.parking_lot_manager_2 import ParkingLotManager, Gate
from ParkingLot.pricing_strategy_5 import PricingStrategyFactory
from ParkingLot.parking_spot_1 import HandicappedSpot, CompactSpot, LargeSpot, TruckSpot
from ParkingLot.parking_terminal_4 import  EntryTerminal, ExitTerminal


if __name__ == "__main__":
    # STEP 1: Setup Parking Lot
    manager = ParkingLotManager.get_instance()

    # Add two gates
    gate_a = Gate("gate-A", "East Gate")
    gate_b = Gate("gate-B", "West Gate")
    manager.add_gate(gate_a)
    manager.add_gate(gate_b)

    # STEP 2: Add parking spots
    # For simplicity, add 2 spots of each type near each gate
    for i in range(2):
        manager.add_parking_spot("gate-A", HandicappedSpot(), distance_from_gate=5 + i)
        manager.add_parking_spot("gate-A", CompactSpot(), distance_from_gate=10 + i)
        manager.add_parking_spot("gate-A", LargeSpot(), distance_from_gate=15 + i)
        manager.add_parking_spot("gate-A", TruckSpot(), distance_from_gate=20 + i)

        manager.add_parking_spot("gate-B", HandicappedSpot(), distance_from_gate=6 + i)
        manager.add_parking_spot("gate-B", CompactSpot(), distance_from_gate=11 + i)
        manager.add_parking_spot("gate-B", LargeSpot(), distance_from_gate=16 + i)
        manager.add_parking_spot("gate-B", TruckSpot(), distance_from_gate=21 + i)

    # STEP 3: Entry simulation
    entry_terminal_a = EntryTerminal("entry-1", "gate-A")
    entry_terminal_b = EntryTerminal("entry-2", "gate-B")

    print("\n--- Vehicles Enter ---")
    ticket1 = entry_terminal_a.get_ticket("Compact")
    ticket2 = entry_terminal_b.get_ticket("Truck")
    ticket3 = entry_terminal_a.get_ticket("Handicapped")

    # Fake a wait to simulate time passage
    time.sleep(2)

    # STEP 4: Exit simulation
    exit_terminal = ExitTerminal("exit-1", "gate-A")

    print("\n--- Vehicles Exit ---")
    for ticket in [ticket1, ticket2, ticket3]:
        if ticket:
            # Fake ticket.issue_time to simulate past time
            ticket.issue_time -= timedelta(hours=3)  # Pretend each stayed 3 hours
            strategy = PricingStrategyFactory.get_strategy(ticket.parking_spot_type)
            hours_parked = 3
            price = strategy.calculate_price(hours_parked)

            ticket.mark_exit(ticket.issue_time + timedelta(hours=hours_parked))
            ticket.mark_paid(price)
            manager.release_spot_by_id(ticket.parking_spot_id)

            print(f"Ticket {ticket.ticket_id}: {ticket.parking_spot_type} → ₹{price} for {hours_parked} hours")

    print("\n✅ Simulation Complete.")
