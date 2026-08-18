from decimal import Decimal, ROUND_HALF_UP

# Deterministic illustrative USD-per-local-unit reporting rates for the take-home.
# These are NOT live market rates. Production should use finance-approved, versioned rates.
FX_TO_USD = {
    "USD": Decimal("1.000000"),
    "INR": Decimal("0.011500"),
    "GBP": Decimal("1.290000"),
    "EUR": Decimal("1.160000"),
    "SGD": Decimal("0.780000"),
    "CAD": Decimal("0.725000"),
    "AUD": Decimal("0.650000"),
    "JPY": Decimal("0.006800"),
}

SUPPORTED_CURRENCIES = tuple(FX_TO_USD.keys())


def get_reporting_rate(currency: str) -> Decimal:
    try:
        return FX_TO_USD[currency.upper()]
    except KeyError as exc:
        raise ValueError(f"Unsupported currency: {currency}") from exc


def normalize_to_usd(amount: Decimal, rate: Decimal) -> Decimal:
    return (amount * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
