"""
Generate safe mock stock prices for the Algo Trading V1 project.
"""

import math
import random

from config import START_PRICE


_current_price: float = START_PRICE


def generate_mock_price() -> float:
    """
    Generate and return the next mock stock price.

    The new price moves randomly by up to 1% from the previous price.
    Invalid prices are safely reset to the configured starting price.
    """
    global _current_price

    if not math.isfinite(_current_price) or _current_price <= 0:
        _current_price = START_PRICE

    percentage_change: float = random.uniform(-1.0, 1.0)
    price_change: float = _current_price * (percentage_change / 100)

    new_price: float = _current_price + price_change
    _current_price = round(max(new_price, 0.01), 2)

    return _current_price