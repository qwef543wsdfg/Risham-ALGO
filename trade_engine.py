"""
Paper-trade execution engine.

This module converts BUY and SELL signals into simulated trades.
It updates the portfolio but does not generate market signals.
"""

import csv
import math
from datetime import datetime
from pathlib import Path

from config import STOCK_SYMBOL, TRADES_FILE_PATH
from portfolio import load_portfolio, save_portfolio


from risk_manager import (
    calculate_buy_quantity,
    calculate_stop_loss_price,
    validate_sell_quantity,
)


TRADE_FIELDS = [
    "timestamp",
    "symbol",
    "side",
    "price",
    "quantity",
    "trade_value",
    "stop_loss_price",
    "average_entry_price",
    "realized_pnl",
]



def save_trade(
    trade_details: dict[str, object],
) -> tuple[bool, str]:
    """
    Append one successful paper trade to trades.csv.

    Args:
        trade_details: Dictionary containing executed trade data.

    Returns:
        A tuple containing success status and a message.
    """
    required_fields = [
        "side",
        "price",
        "quantity",
        "trade_value",
        "realized_pnl",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in trade_details
    ]

    if missing_fields:
        return False, (
            "Trade is missing required fields: "
            + ", ".join(missing_fields)
        )

    try:
        trade_path = Path(TRADES_FILE_PATH)
        trade_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_is_empty = (
            not trade_path.exists()
            or trade_path.stat().st_size == 0
        )

        trade_row = {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "symbol": STOCK_SYMBOL,
            "side": trade_details["side"],
            "price": trade_details["price"],
            "quantity": trade_details["quantity"],
            "trade_value": trade_details["trade_value"],
            "stop_loss_price": trade_details.get(
                "stop_loss_price",
                "",
            ),
            "average_entry_price": trade_details.get(
                "average_entry_price",
                "",
            ),
            "realized_pnl": trade_details["realized_pnl"],
        }

        with trade_path.open(
            mode="a",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=TRADE_FIELDS,
            )

            if file_is_empty:
                writer.writeheader()

            writer.writerow(trade_row)

        return True, "Trade saved successfully."

    except (OSError, csv.Error) as error:
        return False, f"Could not save trade: {error}"



def read_recent_trades(
    limit: int = 10,
) -> list[dict[str, str]]:
    """
    Read the most recent executed paper trades.

    Args:
        limit: Maximum number of trade rows to return.

    Returns:
        A list of trade dictionaries.
        Returns an empty list when no valid trade history exists.
    """
    if not isinstance(limit, int) or limit <= 0:
        return []

    trade_path = Path(TRADES_FILE_PATH)

    if not trade_path.exists() or trade_path.stat().st_size == 0:
        return []

    try:
        with trade_path.open(
            mode="r",
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)
            trades = list(reader)

        valid_trades = [
            trade
            for trade in trades
            if all(field in trade for field in TRADE_FIELDS)
        ]

        return valid_trades[-limit:]

    except (OSError, csv.Error):
        return []




def execute_buy(
    price: float,
) -> tuple[bool, dict[str, object] | None, str]:
    """
    Execute a paper BUY trade.

    Args:
        price: Current market price per share.

    Returns:
        A tuple containing:
        - Success status
        - Trade details when successful, otherwise None
        - Status or error message
    """
    if not isinstance(price, (int, float)):
        return False, None, "BUY price must be numeric."

    if not math.isfinite(float(price)) or price <= 0:
        return False, None, "BUY price must be positive and finite."

    portfolio, portfolio_message = load_portfolio()

    if portfolio is None:
        return False, None, portfolio_message

    current_quantity = int(portfolio["quantity"])

    if current_quantity > 0:
        return (
            False,
            None,
            "BUY rejected because a position is already open.",
        )

    cash = float(portfolio["cash"])

    approved_quantity, risk_message = calculate_buy_quantity(
        cash=cash,
        entry_price=float(price),
    )

    if approved_quantity <= 0:
        return False, None, risk_message

    trade_value = approved_quantity * float(price)

    updated_portfolio = portfolio.copy()

    updated_portfolio["cash"] = round(
        cash - trade_value,
        2,
    )
    updated_portfolio["quantity"] = approved_quantity
    updated_portfolio["average_price"] = round(
        float(price),
        2,
    )

    saved, save_message = save_portfolio(
        updated_portfolio
    )

    if not saved:
        return False, None, save_message

    trade_details: dict[str, object] = {
        "side": "BUY",
        "price": round(float(price), 2),
        "quantity": approved_quantity,
        "trade_value": round(trade_value, 2),
        "stop_loss_price": calculate_stop_loss_price(
            float(price)
        ),
        "average_entry_price": round(float(price), 2),
        "realized_pnl": 0.0,
    }




    trade_saved, trade_save_message = save_trade(
        trade_details
    )

    if not trade_saved:
        return (
            False,
            trade_details,
            (
                "BUY portfolio was updated, but trade history "
                f"could not be saved. {trade_save_message}"
            ),
        )

    return (
        True,
        trade_details,
        f"BUY executed successfully. {risk_message}",
    )


def execute_sell(
    price: float,
) -> tuple[bool, dict[str, object] | None, str]:
    """
    Close the complete open paper-trading position.

    Args:
        price: Current market price per share.

    Returns:
        A tuple containing:
        - Success status
        - Trade details when successful, otherwise None
        - Status or error message
    """
    if not isinstance(price, (int, float)):
        return False, None, "SELL price must be numeric."

    if not math.isfinite(float(price)) or price <= 0:
        return False, None, "SELL price must be positive and finite."

    portfolio, portfolio_message = load_portfolio()

    if portfolio is None:
        return False, None, portfolio_message

    current_quantity = int(portfolio["quantity"])

    valid_sell, validation_message = validate_sell_quantity(
        current_quantity=current_quantity,
        requested_quantity=current_quantity,
    )

    if not valid_sell:
        return False, None, validation_message

    average_price = float(portfolio["average_price"])
    cash = float(portfolio["cash"])
    previous_realized_pnl = float(
        portfolio["realized_pnl"]
    )

    sale_value = current_quantity * float(price)

    trade_pnl = (
        float(price) - average_price
    ) * current_quantity

    updated_portfolio = portfolio.copy()

    updated_portfolio["cash"] = round(
        cash + sale_value,
        2,
    )
    updated_portfolio["quantity"] = 0
    updated_portfolio["average_price"] = 0.0
    updated_portfolio["realized_pnl"] = round(
        previous_realized_pnl + trade_pnl,
        2,
    )

    saved, save_message = save_portfolio(
        updated_portfolio
    )

    if not saved:
        return False, None, save_message

    trade_details: dict[str, object] = {
        "side": "SELL",
        "price": round(float(price), 2),
        "quantity": current_quantity,
        "trade_value": round(sale_value, 2),
        "average_entry_price": round(
            average_price,
            2,
        ),
        "realized_pnl": round(trade_pnl, 2),
    }
     
    trade_saved, trade_save_message = save_trade(
        trade_details
    )

    if not trade_saved:
        return (
            False,
            trade_details,
            (
                "SELL portfolio was updated, but trade history "
                f"could not be saved. {trade_save_message}"
            ),
        )

    return (
        True,
        trade_details,
        "SELL executed successfully.",
    )


    return (
        True,
        trade_details,
        "SELL executed successfully.",
    )


def execute_signal(
    signal: str,
    price: float,
) -> tuple[bool, dict[str, object] | None, str]:
    """
    Route a trading signal to the correct execution function.

    Args:
        signal: BUY, SELL, or HOLD.
        price: Current market price.

    Returns:
        Execution status, optional trade details, and message.
    """
    if not isinstance(signal, str):
        return False, None, "Signal must be a string."

    normalized_signal = signal.strip().upper()

    if normalized_signal == "BUY":
        return execute_buy(price)

    if normalized_signal == "SELL":
        return execute_sell(price)

    if normalized_signal == "HOLD":
        return (
            True,
            None,
            "HOLD signal received. No trade executed.",
        )

    return (
        False,
        None,
        f"Unsupported signal: {signal}",
    )