"""Rental system manager.

Owns the fleet of vehicles and exposes high-level operations: listing
availability, renting and returning by id, and computing cost via the
polymorphic ``rental_cost`` of each vehicle.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Optional

from vehicles import Vehicle


class RentalSystem:
    """Manages a collection of vehicles and rental transactions."""

    def __init__(self, vehicles: Optional[Iterable[Vehicle]] = None) -> None:
        self._fleet: dict[str, Vehicle] = {}
        if vehicles:
            for vehicle in vehicles:
                self.add_vehicle(vehicle)

    def add_vehicle(self, vehicle: Vehicle) -> None:
        """Register a vehicle in the fleet."""
        if vehicle.vehicle_id in self._fleet:
            raise ValueError(f"Vehicle {vehicle.vehicle_id} already exists.")
        self._fleet[vehicle.vehicle_id] = vehicle

    def get_vehicle(self, vehicle_id: str) -> Vehicle:
        vid = vehicle_id.strip().upper()
        if vid not in self._fleet:
            raise KeyError(f"No vehicle with id {vid}.")
        return self._fleet[vid]

    def available_vehicles(self) -> list[Vehicle]:
        return [v for v in self._fleet.values() if not v.is_rented]

    def rented_vehicles(self) -> list[Vehicle]:
        return [v for v in self._fleet.values() if v.is_rented]

    def list_availability(self) -> None:
        if not self._fleet:
            print("No vehicles in the fleet.")
            return
        for vehicle in self._fleet.values():
            print(vehicle.display_availability())

    def rent(self, vehicle_id: str, days: int) -> float:
        """Rent a vehicle and return the computed total cost."""
        vehicle = self.get_vehicle(vehicle_id)
        vehicle.rent()
        cost = vehicle.rental_cost(days)
        print(f"Rented {vehicle.vehicle_id} for {days} day(s): {cost:.2f}")
        return cost

    def return_vehicle(self, vehicle_id: str) -> None:
        """Return a rented vehicle."""
        vehicle = self.get_vehicle(vehicle_id)
        vehicle.return_vehicle()
        print(f"Returned {vehicle.vehicle_id}.")
