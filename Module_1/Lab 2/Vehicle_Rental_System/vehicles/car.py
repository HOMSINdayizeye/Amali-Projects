"""Car vehicle subclass."""

from __future__ import annotations

from .vehicle import Vehicle


class Car(Vehicle):
    """A car rental.

    Pricing: daily base rate plus a flat insurance surcharge per day.
    Cars also expose the number of seats and whether they have A/C.
    """

    def __init__(
        self,
        vehicle_id: str,
        brand: str,
        model: str,
        base_rate: float,
        seats: int = 5,
        has_ac: bool = True,
        insurance_per_day: float = 15.0,
    ) -> None:
        super().__init__(vehicle_id, brand, model, base_rate)
        self.seats = seats
        self.has_ac = has_ac
        self.insurance_per_day = insurance_per_day

    @property
    def vehicle_type(self) -> str:
        return "Car"

    @property
    def rental_price(self) -> float:
        # Displayed price includes the daily insurance surcharge.
        return self.base_rate + self.insurance_per_day

    def rental_cost(self, days: int) -> float:
        if days <= 0:
            raise ValueError("Rental days must be positive")
        daily = self.base_rate + self.insurance_per_day
        # Weekly discount: every 7th day is free.
        free_days = days // 7
        return round(daily * (days - free_days), 2)
