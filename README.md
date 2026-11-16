# Python Internship Project: Interactive Calculator & Unit Converter

**Author / Intern:** Yashraj  
**Environment:** Python 3.10+  
**Dependencies:** None (Python Standard Library only)  

---

## 1. Project Overview

For this internship assignment, I built a modular console application that pairs a standard arithmetic calculator with unit and forex converters. The user interacts through a continuous menu loop, allowing multiple operations in one session until they choose to exit.

To go a step further, I also included a lightweight web interface in `server.py` using Python's built-in `http.server` module. This allows the same conversion and calculation logic to run in a web browser on `http://localhost:8000` without installing Flask or any third-party pip packages.

---

## 2. Project Architecture & File Layout

Rather than putting all the code in a single script, I divided the logic into separate modules so that each file has a single responsibility:

* **`main.py`**: The main entry point. Houses the top-level `while` loop and menu navigation (`if/elif/else`).
* **`calculator.py`**: Contains math functions (`add`, `subtract`, `multiply`, `divide`, `modulus`, `power`) and the arithmetic console sub-menu.
* **`converters.py`**: Handles distance, mass, and temperature conversions using a centralized dictionary `UNIT_FACTORS`.
* **`currency.py`**: Converts currencies using a base rate table (`FOREX_RATES`) anchored to USD.
* **`utils.py`**: Helper functions for reading numeric input safely, validating choices, and formatting text.
* **`server.py`**: A local HTTP server that serves a web UI and handles API calls on `http://localhost:8000`.
* **`test_app.py`**: Automated unit test suite using the `unittest` framework.

---

## 3. Key Design Decisions

### Centralized Dictionaries for Conversion Factors
In `converters.py` and `currency.py`, I avoided hardcoding numeric constants directly inside functions. Instead, I grouped them into dictionary tables:
```python
UNIT_FACTORS = {
    "km_to_miles": 0.621371,
    "miles_to_km": 1.0 / 0.621371,
    "kg_to_lbs": 2.20462,
    "lbs_to_kg": 1.0 / 2.20462,
    "c_to_f_ratio": 1.8,
    "c_to_f_offset": 32.0,
}
```
If a unit factor or exchange rate needs updating later, I only have to edit this single dictionary without touching any calculation logic.

### Base-Currency Anchor for Forex
Instead of creating individual conversion rates between every currency pair (which would require $N \times (N - 1)$ entries), I anchored all foreign currencies to USD (`1.0`). To convert from currency A to currency B:
1. Divide amount by the source currency rate to get equivalent USD.
2. Multiply that USD amount by the target currency rate.

This allows cross-currency conversions (like EUR to INR) while keeping the dictionary compact.

### Defensive Input Handling
One common reason CLI programs crash is bad user input (like typing letters into a numeric prompt). In `utils.py`, `read_float()` wraps `float()` inside a `try/except ValueError` loop. If someone enters non-numeric text, the function catches it, displays a helpful message, and asks again instead of throwing an unhandled traceback.

I also blocked division and modulo by zero directly in the prompt layer and in the core functions using `ZeroDivisionError`.

---

## 4. How to Run the Application

### Running the Terminal CLI
1. Open PowerShell or Terminal.
2. Move into the project directory:
   ```bash
   cd calculator_converter_cli
   ```
3. Run `main.py`:
   ```bash
   python main.py
   ```

### Running the Web Version on Localhost
If you prefer testing the application in a browser:
```bash
python server.py
```
Then visit **`http://localhost:8000`** in your browser.

---

## 5. Running the Unit Tests

I wrote automated unit tests in `test_app.py` covering:
* Arithmetic operations (positive, negative, float values)
* Zero division and zero modulo edge cases
* Exponentiation error on negative base with non-integer power
* Forward and reverse unit conversions (km <-> miles, kg <-> lbs)
* Temperature conversion edge cases ($0^\circ\text{C} = 32^\circ\text{F}$, $-40^\circ\text{C} = -40^\circ\text{F}$)
* Forex conversion math and negative amount validation

Run the tests with:
```bash
python -m unittest test_app.py
```

Expected result:
```text
...........
----------------------------------------------------------------------
Ran 11 tests in 0.002s

OK
```

---

## 6. Sample Console Run

```text
======================================================
 INTERACTIVE CALCULATOR & MULTI-CONVERTER
======================================================
 Console CLI utility for math operations and unit conversions.
 Python standard library only (no external packages needed).
------------------------------------------------------

======================================================
 MAIN MENU
======================================================
  1. Arithmetic Calculator (Add, Sub, Mul, Div, Mod, Exp)
  2. Unit Converter        (Length, Weight, Temperature)
  3. Currency Converter    (USD, EUR, GBP, INR, JPY, etc.)
  4. Exit
------------------------------------------------------
  Enter your selection (1-4): 2

======================================================
 UNIT CONVERTER
======================================================
  Length:
    1. Kilometers to Miles   (km -> mi)
    2. Miles to Kilometers   (mi -> km)
  Weight:
    3. Kilograms to Pounds   (kg -> lbs)
    4. Pounds to Kilograms   (lbs -> kg)
  Temperature:
    5. Celsius to Fahrenheit (°C -> °F)
    6. Fahrenheit to Celsius (°F -> °C)
  7. Return to main menu
------------------------------------------------------
  Select conversion (1-7): 1

  Enter distance in kilometers: 10
------------------------------------------------------
  10.000 km = 6.214 miles
  [Ref: 1 km = 0.621371 mi]
------------------------------------------------------
```
