"""
Helper utilities for user input validation and basic console formatting.
Written for the internship project CLI.
"""

import sys


def show_title(text: str, fill_char: str = "=") -> None:
    """Print a clean section banner in the console."""
    width = 54
    line = fill_char * width
    print(f"\n{line}")
    print(f" {text.upper()}")
    print(f"{line}")


def show_line(length: int = 54) -> None:
    """Small horizontal separator."""
    print("-" * length)


def read_float(
    prompt: str,
    allow_negative: bool = True,
    allow_zero: bool = True,
    custom_zero_msg: str | None = None
) -> float:
    """
    Prompt the user for a numeric float value.
    Keeps asking until the user supplies a valid number.
    """
    while True:
        try:
            raw = input(prompt).strip()
            if not raw:
                print("   [!] Nothing entered. Please type a number.")
                continue

            num = float(raw)

            # Check if zero is blocked (like in division)
            if not allow_zero and num == 0.0:
                msg = custom_zero_msg or "Value cannot be zero here. Try again."
                print(f"   [!] {msg}")
                continue

            # Check if negative numbers are blocked (like distance/weight)
            if not allow_negative and num < 0:
                print("   [!] Negative numbers are not allowed for this field.")
                continue

            return num

        except ValueError:
            print("   [!] That wasn't a valid number (e.g. try 12, -4.5, 0.25).")
        except (KeyboardInterrupt, EOFError):
            print("\n   [!] Input cancelled.")
            sys.exit(0)


def read_choice(prompt: str, valid_options: list[str]) -> str:
    """
    Ensure the user picks an option from the allowed list.
    Case-insensitive matching.
    """
    cleaned_options = [opt.strip().upper() for opt in valid_options]
    while True:
        try:
            user_val = input(prompt).strip().upper()
            if user_val in cleaned_options:
                return user_val
            opts_str = ", ".join(cleaned_options)
            print(f"   [!] Please choose one of the available options: {opts_str}")
        except (KeyboardInterrupt, EOFError):
            print("\n   [!] Exiting.")
            sys.exit(0)


def wait_for_user() -> None:
    """Pause execution until user presses Enter so they can read the output."""
    try:
        input("\nPress Enter to continue...")
    except (KeyboardInterrupt, EOFError):
        sys.exit(0)
