"""Vehicle Rental System entry point."""

from vehicles import Car, Truck, Bike
from rental_system import RentalSystem


def build_fleet() -> RentalSystem:
    fleet = [
        Car("c001", "Toyota", "Corolla", 40.0, seats=5),
        Truck("t001", "Ford", "F-150", 70.0, capacity_tons=3.0),
        Bike("b001", "Trek", "Marlin", 15.0, electric=False),
    ]
    return RentalSystem(fleet)


def menu() -> None:
    system = build_fleet()
    while True:
        print("\n=== Vehicle Rental System ===")
        print("1. List availability")
        print("2. Rent a vehicle")
        print("3. Return a vehicle")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            system.list_availability()

        elif choice == "2":
            vid = input("Enter vehicle ID to rent: ").strip()
            days_str = input("Enter number of days: ").strip()
            try:
                days = int(days_str)
                system.rent(vid, days)
            except ValueError as exc:
                print(f"Error: {exc}")

        elif choice == "3":
            vid = input("Enter vehicle ID to return: ").strip()
            try:
                system.return_vehicle(vid)
            except (KeyError, RuntimeError) as exc:
                print(f"Error: {exc}")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-4.")


if __name__ == "__main__":
    menu()
