"""Bike vehicle subclass."""

from __future__ import annotations

from .vehicle import Vehicle


class Bike(Vehicle):
    """A bike rental.

    Pricing is calculated hourly (converted from days) and is the cheapest
    option. Bikes are electric or standard.
    """

    def __init__(
        self,
        vehicle_id: str,
        brand: str,
        model: str,
        base_rate: float,
        electric: bool = False,
        hourly_rate: float = 5.0,
    ) -> None:
        super().__init__(vehicle_id, brand, model, base_rate)
        self.electric = electric
        self.hourly_rate = hourly_rate

    @property
    def vehicle_type(self) -> str:
        return "Bike"

    @property
    def rental_price(self) -> float:
        # Expose the hourly rate as the displayed price.
        return self.hourly_rate

    def rental_cost(self, days: int) -> float:
        if days <= 0:
            raise ValueError("Rental days must be positive")
        rate = self.hourly_rate * (1.5 if self.electric else 1.0)
        return round(rate * days, 2)
