"""
Risk management for paper trading.

This module validates whether a trade can be taken and calculates
the maximum safe quantity according to account and risk settings.
It does not execute trades or modify the portfolio.
"""

import math

from config import (
    MAX_POSITION_SIZE_PERCENT,
    RISK_PER_TRADE_PERCENT,
    STOP_LOSS_PERCENT,
)


def calculate_stop_loss_price(
    entry_price: float,
) -> float:
    """
    Calculate the stop-loss price for a long position.

    Args:
        entry_price: Planned buying price of one share.

    Returns:
        Calculated stop-loss price.
    """
    stop_loss_amount = entry_price * (
        STOP_LOSS_PERCENT / 100
    )

    stop_loss_price = entry_price - stop_loss_amount

    return round(stop_loss_price, 2)


def calculate_risk_amount(
    cash: float,
) -> float:
    """
    Calculate the maximum amount allowed to be risked in one trade.

    Args:
        cash: Currently available portfolio cash.

    Returns:
        Maximum allowed risk amount.
    """
    risk_amount = cash * (
        RISK_PER_TRADE_PERCENT / 100
    )

    return round(risk_amount, 2)


def calculate_position_limit(
    cash: float,
) -> float:
    """
    Calculate the maximum money allowed in one position.

    Args:
        cash: Currently available portfolio cash.

    Returns:
        Maximum allowed position value.
    """
    position_limit = cash * (
        MAX_POSITION_SIZE_PERCENT / 100
    )

    return round(position_limit, 2)


def calculate_buy_quantity(
    cash: float,
    entry_price: float,
) -> tuple[int, str]:
    """
    Calculate the maximum safe quantity for a BUY trade.

    The final quantity is limited by:
    - Available cash
    - Risk per trade
    - Maximum position size

    Args:
        cash: Currently available portfolio cash.
        entry_price: Planned buying price per share.

    Returns:
        A tuple containing:
        - Approved integer quantity
        - Explanation message
    """
    if not isinstance(cash, (int, float)):
        return 0, "Cash must be numeric."

    if not isinstance(entry_price, (int, float)):
        return 0, "Entry price must be numeric."

    if not math.isfinite(float(cash)) or cash <= 0:
        return 0, "Cash must be positive and finite."

    if (
        not math.isfinite(float(entry_price))
        or entry_price <= 0
    ):
        return 0, "Entry price must be positive and finite."

    risk_amount = calculate_risk_amount(cash)
    position_limit = calculate_position_limit(cash)

    stop_loss_price = calculate_stop_loss_price(
        entry_price
    )

    risk_per_share = entry_price - stop_loss_price

    if risk_per_share <= 0:
        return 0, "Risk per share must be greater than zero."

    quantity_by_risk = int(
        risk_amount // risk_per_share
    )

    quantity_by_position = int(
        position_limit // entry_price
    )

    quantity_by_cash = int(
        cash // entry_price
    )

    approved_quantity = min(
        quantity_by_risk,
        quantity_by_position,
        quantity_by_cash,
    )

    if approved_quantity <= 0:
        return 0, (
            "Trade rejected because available cash or risk "
            "limits do not allow even one share."
        )

    required_amount = approved_quantity * entry_price

    return approved_quantity, (
        f"Trade approved for {approved_quantity} shares. "
        f"Required amount: ₹{required_amount:.2f}. "
        f"Maximum risk amount: ₹{risk_amount:.2f}."
    )


def validate_sell_quantity(
    current_quantity: int,
    requested_quantity: int,
) -> tuple[bool, str]:
    """
    Validate whether the requested SELL quantity is available.

    Args:
        current_quantity: Shares currently held.
        requested_quantity: Shares requested to be sold.

    Returns:
        A tuple containing validation status and message.
    """
    if not isinstance(current_quantity, int):
        return False, "Current quantity must be an integer."

    if not isinstance(requested_quantity, int):
        return False, "Requested quantity must be an integer."

    if current_quantity < 0:
        return False, "Current quantity cannot be negative."

    if requested_quantity <= 0:
        return False, (
            "Requested SELL quantity must be greater than zero."
        )

    if requested_quantity > current_quantity:
        return False, (
            "SELL rejected because requested quantity exceeds "
            "the available portfolio quantity."
        )

    return True, "SELL quantity is valid."