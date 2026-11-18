"""Held-out tests for T3. Never shown to the model. Run beside the candidate ledger.py."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ledger  # noqa: E402


class NewBehaviour(unittest.TestCase):
    def test_thousands_separators(self):
        for text, cents in [("1,234.50", 123450), ("-1,234,567.8", -123456780), ("1,234", 123400), ("+12,000.07", 1200007)]:
            self.assertEqual(ledger.parse_amount(text), cents, text)

    def test_rejects_more_than_two_decimals(self):
        for text in ("3.505", "0.001", "-1,234.567"):
            with self.assertRaises(ValueError, msg=text):
                ledger.parse_amount(text)

    def test_rejects_malformed_separators(self):
        for text in ("1,23.40", "12,3456", ",123", "1,,234", "1234,567", "1,234,56"):
            with self.assertRaises(ValueError, msg=text):
                ledger.parse_amount(text)


class KeptBehaviour(unittest.TestCase):
    def test_plain_amounts_unchanged(self):
        for text, cents in [("12", 1200), ("3.5", 350), ("-3.50", -350), ("+0.07", 7), ("999", 99900), ("-0.50", -50), ("3.", 300)]:
            self.assertEqual(ledger.parse_amount(text), cents, text)

    def test_garbage_still_raises(self):
        for text in ("abc", "", "1.2.3"):
            with self.assertRaises(ValueError, msg=text):
                ledger.parse_amount(text)

    def test_parse_line_total_and_format(self):
        lines = ["2026-10-01\tCoffee\t-3.50\n", "# a comment\n", "\n", "2026-10-02\t Rent \t1,200.00\n", "2026-10-03\tRefund\t+0.07"]
        self.assertEqual(ledger.parse_line(lines[3]), ("2026-10-02", "Rent", 120000))
        self.assertEqual(ledger.total(lines), 119657)
        self.assertEqual(ledger.format_cents(-350), "-3.50")
        self.assertEqual(ledger.format_cents(123456789), "1234567.89")
        self.assertEqual(ledger.format_cents(7), "0.07")


if __name__ == "__main__":
    unittest.main(verbosity=2)
