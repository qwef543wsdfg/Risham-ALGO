"""
Profit and loss calculations for paper trading.

This module calculates position value, unrealized PnL,
total equity, and account return.
It does not execute trades or modify portfolio data.
"""

import math

from config import INITIAL_CAPITAL


def calculate_position_value(
    current_price: float,
    quantity: int,
) -> float:
    """
    Calculate the current market value of an open position.

    Args:
        current_price: Current price per share.
        quantity: Number of shares currently held.

    Returns:
        Current position value.
    """
    if not isinstance(current_price, (int, float)):
        raise TypeError("Current price must be numeric.")

    if not isinstance(quantity, int):
        raise TypeError("Quantity must be an integer.")

    if (
        not math.isfinite(float(current_price))
        or current_price < 0
    ):
        raise ValueError(
            "Current price must be non-negative and finite."
        )

    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    position_value = float(current_price) * quantity

    return round(position_value, 2)


def calculate_unrealized_pnl(
    current_price: float,
    average_price: float,
    quantity: int,
) -> float:
    """
    Calculate profit or loss on the currently open position.

    Args:
        current_price: Current market price per share.
        average_price: Average buying price per share.
        quantity: Number of shares currently held.

    Returns:
        Unrealized profit or loss.
    """
    if not isinstance(current_price, (int, float)):
        raise TypeError("Current price must be numeric.")

    if not isinstance(average_price, (int, float)):
        raise TypeError("Average price must be numeric.")

    if not isinstance(quantity, int):
        raise TypeError("Quantity must be an integer.")

    numeric_values = {
        "current_price": current_price,
        "average_price": average_price,
    }

    for value_name, value in numeric_values.items():
        if not math.isfinite(float(value)) or value < 0:
            raise ValueError(
                f"{value_name} must be non-negative and finite."
            )

    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    if quantity == 0:
        return 0.0

    unrealized_pnl = (
        float(current_price) - float(average_price)
    ) * quantity

    return round(unrealized_pnl, 2)


def calculate_total_equity(
    cash: float,
    current_price: float,
    quantity: int,
) -> float:
    """
    Calculate the current total value of the account.

    Args:
        cash: Available portfolio cash.
        current_price: Current market price per share.
        quantity: Number of shares currently held.

    Returns:
        Current account equity.
    """
    if not isinstance(cash, (int, float)):
        raise TypeError("Cash must be numeric.")

    if not math.isfinite(float(cash)) or cash < 0:
        raise ValueError(
            "Cash must be non-negative and finite."
        )

    position_value = calculate_position_value(
        current_price=current_price,
        quantity=quantity,
    )

    total_equity = float(cash) + position_value

    return round(total_equity, 2)


def calculate_return_percent(
    total_equity: float,
) -> float:
    """
    Calculate account return relative to initial capital.

    Args:
        total_equity: Current total account value.

    Returns:
        Return percentage from the initial capital.
    """
    if not isinstance(total_equity, (int, float)):
        raise TypeError("Total equity must be numeric.")

    if (
        not math.isfinite(float(total_equity))
        or total_equity < 0
    ):
        raise ValueError(
            "Total equity must be non-negative and finite."
        )

    return_percent = (
        (float(total_equity) - INITIAL_CAPITAL)
        / INITIAL_CAPITAL
    ) * 100

    return round(return_percent, 2)


def calculate_portfolio_metrics(
    portfolio: dict[str, float | int],
    current_price: float,
) -> dict[str, float]:
    """
    Calculate all dashboard portfolio metrics together.

    Args:
        portfolio: Current portfolio state.
        current_price: Current market price.

    Returns:
        Dictionary containing calculated portfolio metrics.
    """
    required_fields = [
        "cash",
        "quantity",
        "average_price",
        "realized_pnl",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in portfolio
    ]

    if missing_fields:
        raise KeyError(
            "Portfolio is missing required fields: "
            + ", ".join(missing_fields)
        )

    cash = float(portfolio["cash"])
    quantity = int(portfolio["quantity"])
    average_price = float(portfolio["average_price"])
    realized_pnl = float(portfolio["realized_pnl"])

    position_value = calculate_position_value(
        current_price=current_price,
        quantity=quantity,
    )

    unrealized_pnl = calculate_unrealized_pnl(
        current_price=current_price,
        average_price=average_price,
        quantity=quantity,
    )

    total_equity = calculate_total_equity(
        cash=cash,
        current_price=current_price,
        quantity=quantity,
    )

    return_percent = calculate_return_percent(
        total_equity
    )

    return {
        "cash": round(cash, 2),
        "position_value": position_value,
        "unrealized_pnl": unrealized_pnl,
        "realized_pnl": round(realized_pnl, 2),
        "total_equity": total_equity,
        "return_percent": return_percent,
    }