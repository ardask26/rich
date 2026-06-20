"""Unit tests for rich/filesize module — Part 4 (White-Box Testing).
Project: rich (github.com/Textualize/rich)
Module: rich/filesize.py
Runner: Python unittest (stdlib, no external dependencies required)
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from filesize import decimal, pick_unit_and_suffix, _to_str


class TestDecimalBasicCases(unittest.TestCase):
    """Tests for decimal() covering the core conversion cases."""

    def test_single_byte_returns_special_string(self):
        """Size of exactly 1 must return the singular form '1 byte'."""
        self.assertEqual(decimal(1), "1 byte")

    def test_zero_bytes_formatted_as_bytes(self):
        """Size of 0 is below the base so it should use the 'bytes' plural form."""
        self.assertEqual(decimal(0), "0 bytes")

    def test_value_below_1000_uses_bytes_suffix(self):
        """Any size < 1000 (but != 1) should be formatted with 'bytes'."""
        self.assertEqual(decimal(999), "999 bytes")

    def test_exactly_1000_converts_to_kilobytes(self):
        """1000 bytes is the boundary where kB is used."""
        self.assertEqual(decimal(1000), "1.0 kB")

    def test_megabyte_conversion(self):
        """5 000 000 bytes should render as '5.0 MB'."""
        self.assertEqual(decimal(5_000_000), "5.0 MB")


class TestDecimalFormattingOptions(unittest.TestCase):
    """Tests for precision and separator keyword arguments."""

    def test_precision_zero_removes_decimals(self):
        """precision=0 should produce an integer-style result."""
        result = decimal(30_000, precision=0)
        self.assertEqual(result, "30 kB")

    def test_precision_two_gives_two_decimal_places(self):
        """precision=2 should give exactly two decimal places."""
        self.assertEqual(decimal(30_000, precision=2), "30.00 kB")

    def test_empty_separator_removes_space(self):
        """separator='' should remove the space between number and unit."""
        self.assertEqual(decimal(30_000, separator=""), "30.0kB")

    def test_custom_separator_dash(self):
        """separator='-' should join number and unit with a dash."""
        result = decimal(30_000, separator="-")
        self.assertEqual(result, "30.0-kB")

    def test_gigabyte_conversion(self):
        """1 000 000 000 bytes should render as '1.0 GB'."""
        self.assertEqual(decimal(1_000_000_000), "1.0 GB")


class TestPickUnitAndSuffix(unittest.TestCase):
    """Tests for pick_unit_and_suffix() internal helper."""

    def test_small_value_picks_kb(self):
        """500 bytes with kB/MB/GB list should resolve to kB unit."""
        unit, suffix = pick_unit_and_suffix(500, ["kB", "MB", "GB"], 1000)
        self.assertEqual(suffix, "kB")
        self.assertEqual(unit, 1)

    def test_medium_value_picks_mb(self):
        """500 000 bytes should resolve to MB."""
        unit, suffix = pick_unit_and_suffix(500_000, ["kB", "MB", "GB"], 1000)
        self.assertEqual(suffix, "MB")

    def test_large_value_picks_gb(self):
        """5 000 000 bytes should resolve to GB suffix bucket."""
        unit, suffix = pick_unit_and_suffix(5_000_000, ["kB", "MB", "GB"], 1000)
        self.assertEqual(suffix, "GB")


class TestToStrInternals(unittest.TestCase):
    """Tests for the private _to_str() formatting function."""

    def test_one_returns_singular(self):
        """_to_str with size=1 should short-circuit to '1 byte'."""
        self.assertEqual(_to_str(1, ["kB", "MB"], 1000), "1 byte")

    def test_below_base_returns_bytes_plural(self):
        """_to_str with size < base should use 'bytes' plural."""
        self.assertEqual(_to_str(512, ["kB", "MB"], 1000), "512 bytes")

    def test_above_base_uses_suffix(self):
        """_to_str with size >= base should use the first suffix."""
        result = _to_str(2000, ["kB", "MB"], 1000)
        self.assertIn("kB", result)

    def test_custom_separator_in_to_str(self):
        """separator keyword should appear between value and unit."""
        result = _to_str(2000, ["kB", "MB"], 1000, separator="|")
        self.assertIn("|", result)
        self.assertIn("kB", result)

    def test_precision_controls_decimal_places(self):
        """precision=3 should produce 3 decimal places."""
        result = _to_str(2000, ["kB", "MB"], 1000, precision=3)
        # '2.000 kB'
        decimal_part = result.split(" ")[0].split(".")
        self.assertEqual(len(decimal_part[1]), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
