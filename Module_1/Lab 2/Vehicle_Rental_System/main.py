"""Vehicle Rental System entry point."""

from vehicles import Car, Truck, Bike
from rental_system import RentalSystem


def build_fleet() -> RentalSystem:
    fleet = [
        Car("c001", "Toyota", "Corolla", 40.0, seats=5),
        Truck("t001", "Ford", "F-150", 70.0, capacity_tons=3.0),
        Bike("b001", "Trek", "Marlin", 15.0, electric=True),
    ]
    return RentalSystem(fleet)

def do_add_vehicle(system: RentalSystem) -> None:
    """Prompt the user and add a Car, Truck or Bike to the fleet.

    Cars and Trucks use a daily base rate; Bikes use an hourly rate
    (their base rate is unused), so the relevant rate prompt differs.
    """
    vehicle_id = input("Vehicle ID (e.g. C001): ").strip().upper()
    if not vehicle_id:
        print("Vehicle ID is required.")
        return
    brand = input("Brand: ").strip()
    model = input("Model: ").strip()

    kind = input("Type (1=Car, 2=Truck, 3=Bike): ").strip()
    try:
        if kind == "2":
            base_rate = float(input("Base rate (per day): ").strip())
            capacity = float(input("Capacity (tons): ").strip() or "5")
            vehicle = Truck(vehicle_id, brand, model, base_rate,
                            capacity_tons=capacity)
        elif kind == "3":
            hourly_rate = float(input("Hourly rate: ").strip() or "5")
            electric = input("Electric? (y/N): ").strip().lower() == "y"
            vehicle = Bike(vehicle_id, brand, model, 0.0,
                           electric=electric, hourly_rate=hourly_rate)
        else:
            base_rate = float(input("Base rate (per day): ").strip())
            seats = int(input("Number of seats: ").strip() or "5")
            vehicle = Car(vehicle_id, brand, model, base_rate, seats=seats)
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    try:
        system.add_vehicle(vehicle)
        print(f"Added: {vehicle}")
    except ValueError as exc:
        print(f"Error: {exc}")


def menu() -> None:
    system = build_fleet() # Build the rental system with a fleet of vehicles.
    while True:
        print("\n=== Vehicle Rental System ===")
        print("1. List availability")
        print("2. Rent a vehicle")
        print("3. Return a vehicle")
        print("4. Add a vehicle")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

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
                if vid not in system._fleet:
                    raise KeyError(f"No vehicle with id {vid}.")
                system.return_vehicle(vid)
            except (KeyError, RuntimeError) as exc:
                print(f"Error: {exc}")

        elif choice == "4":
            do_add_vehicle(system)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    menu()
