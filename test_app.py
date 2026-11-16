"""
Unit tests for the math, unit conversion, and forex routines.
Run via: python -m unittest test_app.py
"""

import unittest
from calculator import add, subtract, multiply, divide, modulus, power, clean_num
from converters import (
    UNIT_FACTORS,
    km_to_miles,
    miles_to_km,
    kg_to_lbs,
    lbs_to_kg,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
)
from currency import (
    FOREX_RATES,
    convert_fx,
    get_pair_rate,
)


class TestCalculator(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(add(12, 8), 20)
        self.assertEqual(subtract(20, 5), 15)
        self.assertEqual(multiply(6, 7), 42)
        self.assertEqual(divide(100, 4), 25.0)
        self.assertEqual(modulus(14, 4), 2)
        self.assertEqual(power(2, 4), 16)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(5, 0)
        with self.assertRaises(ZeroDivisionError):
            modulus(5, 0)

    def test_complex_power_error(self):
        # negative base with fraction exponent
        with self.assertRaises(ValueError):
            power(-9, 0.5)

    def test_clean_num_formatting(self):
        self.assertEqual(clean_num(10.0), "10")
        self.assertEqual(clean_num(1250.0), "1,250")
        self.assertEqual(clean_num(3.1415), "3.1415")


class TestConverters(unittest.TestCase):
    def test_length_conversion(self):
        self.assertAlmostEqual(km_to_miles(1), 0.621371, places=5)
        # Reverse check
        miles = km_to_miles(50)
        self.assertAlmostEqual(miles_to_km(miles), 50.0, places=4)

    def test_weight_conversion(self):
        self.assertAlmostEqual(kg_to_lbs(1), 2.20462, places=4)
        # Reverse check
        lbs = kg_to_lbs(20)
        self.assertAlmostEqual(lbs_to_kg(lbs), 20.0, places=4)

    def test_temperature_conversion(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(0), 32.0)
        self.assertAlmostEqual(celsius_to_fahrenheit(100), 212.0)
        self.assertAlmostEqual(celsius_to_fahrenheit(-40), -40.0)
        self.assertAlmostEqual(fahrenheit_to_celsius(32), 0.0)
        self.assertAlmostEqual(fahrenheit_to_celsius(212), 100.0)
        self.assertAlmostEqual(fahrenheit_to_celsius(-40), -40.0)


class TestCurrency(unittest.TestCase):
    def test_supported_rates_present(self):
        for code in ["USD", "EUR", "GBP", "INR"]:
            self.assertIn(code, FOREX_RATES)

    def test_fx_conversion(self):
        self.assertEqual(convert_fx(50, "USD", "USD"), 50.0)
        self.assertEqual(convert_fx(10, "USD", "INR"), 835.0)

    def test_fx_errors(self):
        with self.assertRaises(KeyError):
            convert_fx(10, "XYZ", "USD")
        with self.assertRaises(ValueError):
            convert_fx(-10, "USD", "EUR")

    def test_pair_rate(self):
        self.assertEqual(get_pair_rate("USD", "INR"), 83.50)


if __name__ == "__main__":
    unittest.main()
