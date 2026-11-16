"""
Arithmetic calculator module.
Contains basic math functions and the interactive arithmetic menu.
"""

from utils import read_float, read_choice, show_title, show_line, wait_for_user


def add(x: float, y: float) -> float:
    return x + y


def subtract(x: float, y: float) -> float:
    return x - y


def multiply(x: float, y: float) -> float:
    return x * y


def divide(x: float, y: float) -> float:
    # Explicit check to provide a clean beginner-friendly message
    if y == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return x / y


def modulus(x: float, y: float) -> float:
    if y == 0:
        raise ZeroDivisionError("Cannot calculate modulo with zero as divisor.")
    return x % y


def power(base: float, exponent: float) -> float:
    # If base is negative and exponent has decimal part, Python gives complex (e.g. (-4)**0.5)
    if base < 0 and not exponent.is_integer():
        raise ValueError("Negative numbers cannot have fractional exponents (results in complex numbers).")
    try:
        return base ** exponent
    except OverflowError:
        raise OverflowError("Number too large to calculate.")


def clean_num(n: float) -> str:
    """Helper to display integers cleanly without the .0 suffix."""
    if n.is_integer():
        return f"{int(n):,}"
    # up to 6 decimal places, remove useless trailing zeros
    return f"{n:,.6f}".rstrip("0").rstrip(".")


def calculator_menu() -> None:
    """Sub-menu for arithmetic operations. Loops until the user returns."""
    while True:
        show_title("Arithmetic Calculator")
        print("  1. Addition       (+)")
        print("  2. Subtraction    (-)")
        print("  3. Multiplication (*)")
        print("  4. Division       (/)")
        print("  5. Modulus        (%)")
        print("  6. Exponentiation (^)")
        print("  7. Return to main menu")
        show_line()

        pick = read_choice("  Select operation (1-7): ", ["1", "2", "3", "4", "5", "6", "7"])

        if pick == "7":
            print("\n  Heading back to main menu...")
            break

        print()
        first = read_float("  Enter first number: ")

        # Block zero upfront if division or modulo was chosen
        if pick == "4":
            second = read_float("  Enter divisor (second number): ", allow_zero=False,
                                custom_zero_msg="Division by zero is not allowed. Try another number.")
        elif pick == "5":
            second = read_float("  Enter divisor (second number): ", allow_zero=False,
                                custom_zero_msg="Modulo by zero is not allowed. Try another number.")
        else:
            second = read_float("  Enter second number: ")

        try:
            if pick == "1":
                out = add(first, second)
                op = "+"
            elif pick == "2":
                out = subtract(first, second)
                op = "-"
            elif pick == "3":
                out = multiply(first, second)
                op = "*"
            elif pick == "4":
                out = divide(first, second)
                op = "/"
            elif pick == "5":
                out = modulus(first, second)
                op = "%"
            elif pick == "6":
                out = power(first, second)
                op = "^"
            else:
                print("  [!] Option not recognized.")
                continue

            show_line()
            print(f"  Result: {clean_num(first)} {op} {clean_num(second)} = {clean_num(out)}")
            show_line()

        except ZeroDivisionError as err:
            print(f"\n  [Error] {err}")
        except ValueError as err:
            print(f"\n  [Error] {err}")
        except OverflowError as err:
            print(f"\n  [Error] {err}")

        wait_for_user()
