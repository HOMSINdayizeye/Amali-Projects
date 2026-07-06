# Vehicle Rental System

A Python project demonstrating **OOP fundamentals**: abstract base classes,
inheritance, polymorphism, and property decorators through a simple vehicle
rental simulation (cars, trucks, and bikes).

## Learning objectives covered

- Python data structures & functions for real-world simulation
- Classes with **inheritance** and **polymorphism**
- **Property decorators** for rental state and price management
- **Abstract base classes** (`abc.ABC`) for uniform rental operations
- Clean module organization and naming conventions

## Project structure

```
Vehicle_Rental_System/
├── main.py              # Demo entry point (run to see it work)
├── rental_system.py     # RentalSystem: fleet management & operations
├── vehicles/            # Package of vehicle classes
│   ├── vehicle.py       # Abstract Vehicle base class (ABC)
│   ├── car.py           # Car subclass (daily rate + insurance)
│   ├── truck.py         # Truck subclass (rate scales with capacity)
│   ├── bike.py          # Bike subclass (hourly rate, electric option)
│   └── __init__.py      # Public API exports
├── tests/
│   └── test_rental.py   # pytest test suite
├── requirements.txt     # Project dependencies
└── .gitignore
```

## Design highlights

| Concept | Where |
| --- | --- |
| Abstract base class | `vehicles/vehicle.py` — `Vehicle(ABC)` defines the contract |
| Polymorphic pricing | each subclass implements `rental_cost(days)` differently |
| Property decorators | `is_rented`, `rental_price`, `vehicle_type` are read-only properties |
| State management | `_is_rented` flag toggled by `rent()` / `return_vehicle()` |
| Collections | `RentalSystem` stores the fleet in a `dict` by `vehicle_id` |

### Pricing logic (polymorphic)
- **Car** — `(base_rate + insurance/day) × days`, with every 7th day free.
- **Truck** — `(base_rate + load_fee × capacity_tons) × days`.
- **Bike** — `hourly_rate × 24 × days` (electric bikes cost 1.5×).

## Setup (you manage the venv)

```bash
# 1. Create & activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the demo
python main.py

# 4. Run the tests
python -m pytest tests/ -q
```

## Extending the system

Add a new vehicle type by subclassing `Vehicle` and implementing the two
abstract properties/methods:

```python
from vehicles import Vehicle

class Scooter(Vehicle):
    @property
    def vehicle_type(self) -> str:
        return "Scooter"

    def rental_cost(self, days: int) -> float:
        return round(self.base_rate * days, 2)
```
