"""
Portfolio state management.

This module creates, saves, and loads the paper-trading portfolio.
It does not generate signals or execute trades.
"""

import csv
from pathlib import Path

from config import INITIAL_CAPITAL, PORTFOLIO_FILE_PATH


PORTFOLIO_FIELDS = [
    "cash",
    "quantity",
    "average_price",
    "realized_pnl",
]


def create_default_portfolio() -> dict[str, float | int]:
    """
    Create the initial paper-trading portfolio.

    Returns:
        A dictionary containing the starting portfolio state.
    """
    return {
        "cash": float(INITIAL_CAPITAL),
        "quantity": 0,
        "average_price": 0.0,
        "realized_pnl": 0.0,
    }


def save_portfolio(
    portfolio: dict[str, float | int],
) -> tuple[bool, str]:
    """
    Save the current portfolio state to portfolio.csv.

    Args:
        portfolio: Dictionary containing current portfolio values.

    Returns:
        A tuple containing success status and a message.
    """
    missing_fields = [
        field
        for field in PORTFOLIO_FIELDS
        if field not in portfolio
    ]

    if missing_fields:
        return False, (
            "Portfolio is missing required fields: "
            + ", ".join(missing_fields)
        )

    try:
        portfolio_path = Path(PORTFOLIO_FILE_PATH)
        portfolio_path.parent.mkdir(parents=True, exist_ok=True)

        with portfolio_path.open(
            mode="w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=PORTFOLIO_FIELDS,
            )

            writer.writeheader()
            writer.writerow(portfolio)

        return True, "Portfolio saved successfully."

    except (OSError, csv.Error) as error:
        return False, f"Could not save portfolio: {error}"


def initialize_portfolio() -> tuple[bool, str]:
    """
    Create portfolio.csv when it does not contain portfolio data.

    Existing portfolio data is preserved.
    """
    portfolio_path = Path(PORTFOLIO_FILE_PATH)

    if portfolio_path.exists() and portfolio_path.stat().st_size > 0:
        return True, "Portfolio already exists."

    default_portfolio = create_default_portfolio()

    return save_portfolio(default_portfolio)


def load_portfolio() -> tuple[
    dict[str, float | int] | None,
    str,
]:
    """
    Load the current portfolio state from portfolio.csv.

    Returns:
        A tuple containing:
        - Portfolio dictionary when loading succeeds.
        - None when loading fails.
        - Status or error message.
    """
    initialized, initialization_message = initialize_portfolio()

    if not initialized:
        return None, initialization_message

    try:
        portfolio_path = Path(PORTFOLIO_FILE_PATH)

        with portfolio_path.open(
            mode="r",
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)
            row = next(reader, None)

        if row is None:
            return None, "Portfolio file does not contain any data."

        portfolio = {
            "cash": float(row["cash"]),
            "quantity": int(row["quantity"]),
            "average_price": float(row["average_price"]),
            "realized_pnl": float(row["realized_pnl"]),
        }

        return portfolio, "Portfolio loaded successfully."

    except KeyError as error:
        return None, f"Portfolio column is missing: {error}"

    except ValueError as error:
        return None, f"Portfolio contains invalid numeric data: {error}"

    except (OSError, csv.Error) as error:
        return None, f"Could not load portfolio: {error}"