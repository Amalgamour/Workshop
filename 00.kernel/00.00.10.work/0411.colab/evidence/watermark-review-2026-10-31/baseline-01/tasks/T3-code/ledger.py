"""Tiny ledger: tab-separated lines of date, description and amount."""


def parse_amount(text):
    """Return the amount in cents as an int."""
    sign = -1 if text.startswith("-") else 1
    text = text.lstrip("+-")
    whole, _, frac = text.partition(".")
    return sign * (int(whole) * 100 + int((frac + "00")[:2]))


def parse_line(line):
    """Return (date, description, cents) for one ledger line."""
    date, description, amount = line.rstrip("\n").split("\t")
    return date, description.strip(), parse_amount(amount.strip())


def total(lines):
    """Sum the amounts of all lines, skipping blank lines and # comments."""
    cents = 0
    for line in lines:
        if line.strip() and not line.lstrip().startswith("#"):
            cents += parse_line(line)[2]
    return cents


def format_cents(cents):
    """Format cents as a signed decimal string, e.g. -350 -> '-3.50'."""
    sign = "-" if cents < 0 else ""
    return f"{sign}{abs(cents) // 100}.{abs(cents) % 100:02d}"
