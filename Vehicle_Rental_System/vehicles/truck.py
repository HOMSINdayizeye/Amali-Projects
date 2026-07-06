"""Truck vehicle subclass."""

from __future__ import annotations

from .vehicle import Vehicle


class Truck(Vehicle):
    """A truck rental.

    Pricing: daily base rate plus a per-day load fee that scales with the
    truck's cargo capacity (tonnes).
    """

    def __init__(
        self,
        vehicle_id: str,
        brand: str,
        model: str,
        base_rate: float,
        capacity_tons: float = 5.0,
        load_fee_per_day: float = 10.0,
    ) -> None:
        super().__init__(vehicle_id, brand, model, base_rate)
        self.capacity_tons = capacity_tons
        self.load_fee_per_day = load_fee_per_day

    @property
    def vehicle_type(self) -> str:
        return "Truck"

    @property
    def rental_price(self) -> float:
        return self.base_rate + self.load_fee_per_day * self.capacity_tons

    def rental_cost(self, days: int) -> float:
        if days <= 0:
            raise ValueError("Rental days must be positive")
        daily = self.base_rate + self.load_fee_per_day * self.capacity_tons
        return round(daily * days, 2)
