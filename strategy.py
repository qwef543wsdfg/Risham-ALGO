"""
Apply trading rules and return BUY, SELL, or HOLD signals.
"""

import math

from config import BUY_THRESHOLD, SELL_THRESHOLD


def generate_signal(price: float) -> str:
    """
    Return a trading signal for the supplied price.

    Invalid prices return HOLD so the program can continue safely.
    """
    if not isinstance(price, (int, float)):
        return "HOLD"

    numeric_price: float = float(price)

    if not math.isfinite(numeric_price) or numeric_price <= 0:
        return "HOLD"

    if numeric_price > BUY_THRESHOLD:
        return "BUY"

    if numeric_price < SELL_THRESHOLD:
        return "SELL"

    return "HOLD"