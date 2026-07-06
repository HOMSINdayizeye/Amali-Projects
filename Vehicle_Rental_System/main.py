"""Vehicle Rental System - interactive entry point.

Run with:  python main.py
Provides an interactive menu to list, rent, and return vehicles.
"""

from rental_system import RentalSystem
from vehicles import Bike, Car, Truck


def build_fleet() -> RentalSystem:
    system = RentalSystem()
    system.add_vehicle(Car("CAR-001", "Toyota", "Corolla", 40.0, seats=5))
    system.add_vehicle(Car("CAR-002", "Tesla", "Model 3", 70.0, seats=5, insurance_per_day=25.0))
    system.add_vehicle(Truck("TRK-001", "Volvo", "FH16", 90.0, capacity_tons=18.0))
    system.add_vehicle(Bike("BIK-001", "Giant", "Escape", 0.0, hourly_rate=5.0))
    system.add_vehicle(Bike("BIK-002", "Specialized", "Turbo", 0.0, electric=True, hourly_rate=8.0))
    return system


def show_menu() -> None:
    print("\n--- Vehicle Rental System ---")
    print("1. List availability")
    print("2. Rent a vehicle")
    print("3. Return a vehicle")
    print("4. Exit")


def interactive(system: RentalSystem) -> None:
    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()
        if choice == "1":
            system.list_availability()
        elif choice == "2":
            vid = input("Enter vehicle ID to rent: ").strip()
            days = input("Enter number of days: ").strip()
            try:
                days = int(days)
                system.rent(vid, days)
            except (ValueError, KeyError, RuntimeError) as err:
                print(f"Error: {err}")
        elif choice == "3":
            vid = input("Enter vehicle ID to return: ").strip()
            try:
                system.return_vehicle(vid)
            except (KeyError, RuntimeError) as err:
                print(f"Error: {err}")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-4.")


def main() -> None:
    system = build_fleet()
    system.list_availability()
    interactive(system)


if __name__ == "__main__":
    main()
