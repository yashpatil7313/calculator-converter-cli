"""
CLI Application: Interactive Calculator & Unit Converter
Internship Project - Python 3.10+
"""

import sys
from calculator import calculator_menu
from converters import unit_converter_menu
from currency import currency_converter_menu
from utils import read_choice, show_line, show_title


def main() -> None:
    """Main program entry loop."""
    show_title("Interactive Calculator & Multi-Converter")
    print(" Console CLI utility for math operations and unit conversions.")
    print(" Python standard library only (no external packages needed).")
    show_line()

    while True:
        show_title("Main Menu")
        print("  1. Arithmetic Calculator (Add, Sub, Mul, Div, Mod, Exp)")
        print("  2. Unit Converter        (Length, Weight, Temperature)")
        print("  3. Currency Converter    (USD, EUR, GBP, INR, JPY, etc.)")
        print("  4. Exit")
        show_line()

        user_choice = read_choice("  Enter your selection (1-4): ", ["1", "2", "3", "4"])

        if user_choice == "1":
            calculator_menu()
        elif user_choice == "2":
            unit_converter_menu()
        elif user_choice == "3":
            currency_converter_menu()
        elif user_choice == "4":
            print("\n  Thank you for using the tool. Goodbye!\n")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n  Session closed by user. Exiting cleanly.")
        sys.exit(0)
