"""Base Vehicle abstract class.

Defines the contract that every rentable vehicle must follow and provides
shared state management (available vs rented) and common operations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Vehicle(ABC):
    """Abstract base class for all rentable vehicles.

    Subclasses must implement :meth:`rental_cost`, which computes the price
    for a given rental duration. State (rented vs available) is managed
    through a private attribute exposed via a read-only property.
    """

    vehicle_id: str
    brand: str
    model: str
    base_rate: float
    _is_rented: bool = field(default=False, repr=False)

    # Default currency used when formatting prices. Subclasses may override.
    currency: ClassVar[str] = "USD"

    def __post_init__(self) -> None:
        if self.base_rate < 0:
            raise ValueError("base_rate must be non-negative")
        self.vehicle_id = self.vehicle_id.strip().upper()

    @property
    def is_rented(self) -> bool:
        """Read-only view of the rental state."""
        return self._is_rented

    @property
    @abstractmethod
    def vehicle_type(self) -> str:
        """Human readable vehicle type (e.g. 'Car', 'Truck', 'Bike')."""
        raise NotImplementedError

    @property
    def rental_price(self) -> float:
        """Per-day displayed base rental price for this vehicle."""
        return self.base_rate

    @abstractmethod
    def rental_cost(self, days: int) -> float:
        """Calculate the total rental cost for ``days`` of rental.

        Must be implemented by each concrete subclass so pricing can
        behave polymorphically across vehicle types.
        """
        raise NotImplementedError

    def rent(self) -> None:
        """Mark the vehicle as rented.

        Raises:
            RuntimeError: if the vehicle is already rented.
        """
        if self._is_rented:
            raise RuntimeError(f"{self.vehicle_id} is already rented.")
        self._is_rented = True

    def return_vehicle(self) -> None:
        """Return the vehicle, making it available again.

        Raises:
            RuntimeError: if the vehicle was not rented.
        """
        if not self._is_rented:
            raise RuntimeError(f"{self.vehicle_id} was not rented.")
        self._is_rented = False

    def display_availability(self) -> str:
        """Return a short availability status string."""
        status = "Rented" if self._is_rented else "Available"
        return f"{self.vehicle_id} ({self.brand} {self.model}) - {status}"

    def __str__(self) -> str:
        return (
            f"{self.vehicle_type}: {self.brand} {self.model} "
            f"[{self.vehicle_id}] - {self.rental_price:.2f} {self.currency}/day"
        )
