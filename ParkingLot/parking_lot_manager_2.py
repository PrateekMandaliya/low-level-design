from collections import defaultdict
from ParkingLot.parking_spot_1 import ParkingSpot
import heapq


class Gate:
    def __init__(self, gate_id, name):
        self.gate_id = gate_id
        self.name = name

    def __repr__(self):
        return f"Gate(id={self.gate_id}, name='{self.name}')"


class ParkingLotManager:
    _instance = None

    @staticmethod
    def get_instance():
        if ParkingLotManager._instance is None:
            ParkingLotManager()
        return ParkingLotManager._instance
    

    def __init__(self):
        if ParkingLotManager._instance is not None:
            raise Exception('Use get_instance() instead of constructor')
        ParkingLotManager._instance = self

        self.gates = {} # gate_id -> Gate object
        self.spots_by_gate_and_type = defaultdict(lambda: defaultdict(list))  # gate_id -> spot_type -> minHeap
        self.spot_id_map = {}  # spot_id → ParkingSpot mapping to release ParkingSpot while exiting

    
    def add_gate(self, gate: Gate):
        self.gates[gate.gate_id] = gate

    
    def add_parking_spot(self, gate_id, spot: ParkingSpot, distance_from_gate: int):
        # We'll use a min-heap to store (distance, spot)
        heapq.heappush(self.spots_by_gate_and_type[gate_id][spot.get_type()], (distance_from_gate, spot))
        self.spot_id_map[spot.spot_id] = spot


    def get_nearest_available_spot(self, gate_id, spot_type):
        spot_heap = self.spots_by_gate_and_type[gate_id][spot_type]
        # Keep popping till I find a available spot
        while spot_heap:
            dist, spot = heapq.heappop(spot_heap)
            if not spot.is_reserved:
                spot.reserve()
                return spot
        return None # No spot available
    

    def release_spot_by_id(self, spot_id):
        spot = self.spot_id_map.get(spot_id)
        if spot:
            spot.release()

