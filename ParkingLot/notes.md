# Functional Requirements

1. Big parking lot 10k-30k spots
2. 4 entrances and exits
3. Parking tickets and spot assigned at the entrance
4. Spots assigned should be near to the entry gate
5. If capacity is full, more cars should not be allowed
6. Four types - handicapped, compact, large, truck
7. Hourly rates
8. Cash and card payments are accepted

# To run, python3 -m ParkingLot.simulation_6 command from one level above ParkingLot folder

# What happens when we have multiple floors for the parking lot?

Before: All spots were grouped by gate_id and spot_type
Now: Spots will be grouped by floor → gate_id → spot_type
ParkingLotManager
├── ParkingFloor (one per level)
│   └── Spots grouped by gate & type (heap)
├── add_parking_spot(floor, gate_id, spot, dist)
└── get_nearest_available_spot(gate_id, spot_type)
        → loop floors → delegate to floor.get_nearest(...)

<!-- 
class ParkingFloor:
    def __init__(self, floor_number):
        self.floor_number = floor_number
        self.spots_by_gate_and_type = defaultdict(lambda: defaultdict(list))  # gate_id → type → minHeap
        self.spot_id_map = {}
    def add_parking_spot(self, gate_id, spot, distance_from_gate):
        pass
    def get_nearest_available_spot(self, gate_id, spot_type):
        pass
    def def release_spot_by_id(self, spot_id):
        pass 
-->