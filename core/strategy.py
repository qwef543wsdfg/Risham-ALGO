"""
Apply the active dashboard strategy and generate trading signals.
"""

import math
from typing import Any

from core.strategy_config import load_strategy_config


VALID_SIGNALS = {
    "BUY",
    "SELL",
    "HOLD",
}


def generate_signal_details(
    price: float,
    strategy_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Generate a detailed signal result for the supplied price.

    The dashboard can use this result to display the signal,
    thresholds, reason, stop loss, and target.
    """

    if not isinstance(price, (int, float)):
        return {
            "signal": "HOLD",
            "reason": "Invalid market price.",
            "price": None,
        }

    numeric_price = float(price)

    if not math.isfinite(numeric_price) or numeric_price <= 0:
        return {
            "signal": "HOLD",
            "reason": "Market price must be positive and finite.",
            "price": numeric_price,
        }

    if strategy_config is None:
        strategy_config, _ = load_strategy_config()

    if not strategy_config.get("enabled", False):
        return {
            "signal": "HOLD",
            "reason": "Strategy is currently disabled.",
            "price": numeric_price,
        }

    buy_threshold = float(
        strategy_config["buy_threshold"]
    )

    sell_threshold = float(
        strategy_config["sell_threshold"]
    )

    stop_loss_percent = float(
        strategy_config["stop_loss_percent"]
    )

    target_percent = float(
        strategy_config["target_percent"]
    )

    if numeric_price >= buy_threshold:
        signal = "BUY"
        reason = (
            f"Price ₹{numeric_price:,.2f} crossed above "
            f"buy threshold ₹{buy_threshold:,.2f}."
        )

    elif numeric_price <= sell_threshold:
        signal = "SELL"
        reason = (
            f"Price ₹{numeric_price:,.2f} crossed below "
            f"sell threshold ₹{sell_threshold:,.2f}."
        )

    else:
        signal = "HOLD"
        reason = (
            f"Price is between ₹{sell_threshold:,.2f} and "
            f"₹{buy_threshold:,.2f}."
        )

    stop_loss_price = numeric_price * (
        1 - stop_loss_percent / 100
    )

    target_price = numeric_price * (
        1 + target_percent / 100
    )

    return {
        "signal": signal,
        "reason": reason,
        "price": round(numeric_price, 2),
        "buy_threshold": round(buy_threshold, 2),
        "sell_threshold": round(sell_threshold, 2),
        "stop_loss_price": round(stop_loss_price, 2),
        "target_price": round(target_price, 2),
        "strategy_name": strategy_config["strategy_name"],
        "symbol": strategy_config["symbol"],
        "timeframe": strategy_config["timeframe"],
        "enabled": strategy_config["enabled"],
    }


def generate_signal(price: float) -> str:
    """
    Return only BUY, SELL, or HOLD.

    This function preserves compatibility with the existing dashboard
    and trade engine.
    """

    signal_details = generate_signal_details(price)

    signal = signal_details.get("signal", "HOLD")

    if signal not in VALID_SIGNALS:
        return "HOLD"

    return signal