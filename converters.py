"""
Unit conversion module for length, weight, and temperature.
Stores conversion factors in a central dictionary for easy maintenance.
"""

from utils import read_float, read_choice, show_title, show_line, wait_for_user

# Master lookup dictionary for physical conversion factors.
# Centralizing this means updating a factor here updates it across the entire program.
UNIT_FACTORS = {
    # 1 km = 0.621371 miles
    "km_to_miles": 0.621371,
    # 1 mile = 1 / 0.621371 km (~1.609344 km)
    "miles_to_km": 1.0 / 0.621371,

    # 1 kg = 2.20462 lbs
    "kg_to_lbs": 2.20462,
    # 1 lb = 1 / 2.20462 kg (~0.453592 kg)
    "lbs_to_kg": 1.0 / 2.20462,

    # Temperature constants (scale factor 9/5 = 1.8, offset = 32)
    "c_to_f_ratio": 9.0 / 5.0,
    "c_to_f_offset": 32.0,
}


def km_to_miles(km: float) -> float:
    return km * UNIT_FACTORS["km_to_miles"]


def miles_to_km(miles: float) -> float:
    return miles * UNIT_FACTORS["miles_to_km"]


def kg_to_lbs(kg: float) -> float:
    return kg * UNIT_FACTORS["kg_to_lbs"]


def lbs_to_kg(lbs: float) -> float:
    return lbs * UNIT_FACTORS["lbs_to_kg"]


def celsius_to_fahrenheit(celsius: float) -> float:
    # F = C * (9/5) + 32
    return (celsius * UNIT_FACTORS["c_to_f_ratio"]) + UNIT_FACTORS["c_to_f_offset"]


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    # C = (F - 32) * (5/9)
    return (fahrenheit - UNIT_FACTORS["c_to_f_offset"]) / UNIT_FACTORS["c_to_f_ratio"]


def unit_converter_menu() -> None:
    """Sub-menu for metric/imperial and temperature conversions."""
    while True:
        show_title("Unit Converter")
        print("  Length:")
        print("    1. Kilometers to Miles   (km -> mi)")
        print("    2. Miles to Kilometers   (mi -> km)")
        print("  Weight:")
        print("    3. Kilograms to Pounds   (kg -> lbs)")
        print("    4. Pounds to Kilograms   (lbs -> kg)")
        print("  Temperature:")
        print("    5. Celsius to Fahrenheit (°C -> °F)")
        print("    6. Fahrenheit to Celsius (°F -> °C)")
        print("  7. Return to main menu")
        show_line()

        choice = read_choice("  Select conversion (1-7): ", ["1", "2", "3", "4", "5", "6", "7"])

        if choice == "7":
            print("\n  Heading back to main menu...")
            break

        print()

        # Length conversions (physical distances cannot be negative)
        if choice == "1":
            km = read_float("  Enter distance in kilometers: ", allow_negative=False)
            mi = km_to_miles(km)
            show_line()
            print(f"  {km:,.3f} km = {mi:,.3f} miles")
            print(f"  [Ref: 1 km = {UNIT_FACTORS['km_to_miles']} mi]")
            show_line()

        elif choice == "2":
            mi = read_float("  Enter distance in miles: ", allow_negative=False)
            km = miles_to_km(mi)
            show_line()
            print(f"  {mi:,.3f} miles = {km:,.3f} km")
            print(f"  [Ref: 1 mi = {UNIT_FACTORS['miles_to_km']:.4f} km]")
            show_line()

        # Weight conversions (mass cannot be negative)
        elif choice == "3":
            kg = read_float("  Enter weight in kilograms: ", allow_negative=False)
            lbs = kg_to_lbs(kg)
            show_line()
            print(f"  {kg:,.3f} kg = {lbs:,.3f} lbs")
            print(f"  [Ref: 1 kg = {UNIT_FACTORS['kg_to_lbs']} lbs]")
            show_line()

        elif choice == "4":
            lbs = read_float("  Enter weight in pounds: ", allow_negative=False)
            kg = lbs_to_kg(lbs)
            show_line()
            print(f"  {lbs:,.3f} lbs = {kg:,.3f} kg")
            print(f"  [Ref: 1 lb = {UNIT_FACTORS['lbs_to_kg']:.4f} kg]")
            show_line()

        # Temperature (temperatures can definitely be below zero)
        elif choice == "5":
            c = read_float("  Enter temperature in Celsius: ", allow_negative=True)
            f = celsius_to_fahrenheit(c)
            show_line()
            print(f"  {c:,.2f} °C = {f:,.2f} °F")
            print("  [Formula: F = C * 9/5 + 32]")
            show_line()

        elif choice == "6":
            f = read_float("  Enter temperature in Fahrenheit: ", allow_negative=True)
            c = fahrenheit_to_celsius(f)
            show_line()
            print(f"  {f:,.2f} °F = {c:,.2f} °C")
            print("  [Formula: C = (F - 32) * 5/9]")
            show_line()

        wait_for_user()
