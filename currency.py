"""
Currency converter module.
Uses USD as a base anchor currency to allow cross-conversion between any two currencies.
"""

from utils import read_float, read_choice, show_title, show_line, wait_for_user

# Standard forex rates relative to 1.0 USD base.
# To add a currency, simply insert its code, name, and rate per 1 USD.
FOREX_RATES: dict[str, float] = {
    "USD": 1.00,      # US Dollar (base)
    "EUR": 0.92,      # Euro
    "GBP": 0.79,      # British Pound
    "INR": 83.50,     # Indian Rupee
    "JPY": 155.00,    # Japanese Yen
    "CAD": 1.36,      # Canadian Dollar
    "AUD": 1.52,      # Australian Dollar
}

# (Full Currency Name, Symbol)
FOREX_INFO: dict[str, tuple[str, str]] = {
    "USD": ("US Dollar", "$"),
    "EUR": ("Euro", "€"),
    "GBP": ("British Pound", "£"),
    "INR": ("Indian Rupee", "₹"),
    "JPY": ("Japanese Yen", "¥"),
    "CAD": ("Canadian Dollar", "CA$"),
    "AUD": ("Australian Dollar", "A$"),
}


def convert_fx(amount: float, from_curr: str, to_curr: str) -> float:
    """
    Convert money from one currency to another using the USD base.
    Formula:
      amount_usd = amount / rate[from_curr]
      converted  = amount_usd * rate[to_curr]
    """
    src = from_curr.strip().upper()
    tgt = to_curr.strip().upper()

    if src not in FOREX_RATES:
        raise KeyError(f"Currency '{from_curr}' is not in the supported exchange table.")
    if tgt not in FOREX_RATES:
        raise KeyError(f"Currency '{to_curr}' is not in the supported exchange table.")
    if amount < 0:
        raise ValueError("Currency amounts cannot be negative.")

    # Avoid floating-point arithmetic drift if same currency selected
    if src == tgt:
        return float(amount)

    amount_in_usd = amount / FOREX_RATES[src]
    return amount_in_usd * FOREX_RATES[tgt]


def get_pair_rate(from_curr: str, to_curr: str) -> float:
    """Returns how many units of to_curr equal 1 unit of from_curr."""
    src = from_curr.strip().upper()
    tgt = to_curr.strip().upper()
    return FOREX_RATES[tgt] / FOREX_RATES[src]


def print_rate_sheet() -> None:
    """Prints a neat reference table showing all rates against USD."""
    show_title("Reference Exchange Rates (Per 1 USD)")
    print(f"  {'Code':<6} | {'Symbol':<8} | {'Currency':<18} | {'Rate':>10}")
    show_line()
    for code, rate in FOREX_RATES.items():
        name, symbol = FOREX_INFO.get(code, (code, ""))
        print(f"  {code:<6} | {symbol:<8} | {name:<18} | {rate:>10.2f}")
    show_line()


def currency_converter_menu() -> None:
    """Interactive loop for forex conversions."""
    currencies = list(FOREX_RATES.keys())

    while True:
        show_title("Currency Converter")
        print("  1. Convert between currencies")
        print("  2. View current rate table")
        print("  3. Return to main menu")
        show_line()

        pick = read_choice("  Enter choice (1-3): ", ["1", "2", "3"])

        if pick == "3":
            print("\n  Heading back to main menu...")
            break

        if pick == "2":
            print_rate_sheet()
            wait_for_user()
            continue

        if pick == "1":
            print(f"\n  Supported: {', '.join(currencies)}")
            show_line()

            from_c = read_choice(f"  Convert FROM ({'/'.join(currencies)}): ", currencies)
            to_c = read_choice(f"  Convert TO   ({'/'.join(currencies)}): ", currencies)
            amt = read_float(f"  Enter amount in {from_c}: ", allow_negative=False)

            result = convert_fx(amt, from_c, to_c)
            rate = get_pair_rate(from_c, to_c)

            from_name, from_sym = FOREX_INFO[from_c]
            to_name, to_sym = FOREX_INFO[to_c]

            show_line()
            print("  CONVERSION:")
            print(f"  {from_sym} {amt:,.2f} {from_c} ({from_name})")
            print(f"  = {to_sym} {result:,.2f} {to_c} ({to_name})")
            print(f"  [Exchange rate: 1 {from_c} = {rate:,.4f} {to_c}]")
            show_line()

            wait_for_user()
