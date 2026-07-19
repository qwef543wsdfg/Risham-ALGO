"""
Load, validate, and save dashboard strategy configuration.
"""

import json
import math
from pathlib import Path
from typing import Any

from config import (
    BUY_THRESHOLD,
    MAX_POSITION_SIZE_PERCENT,
    RISK_PER_TRADE_PERCENT,
    SELL_THRESHOLD,
    STOP_LOSS_PERCENT,
    TARGET_PERCENT,
)


STRATEGY_CONFIG_FILE = Path("data/strategy_config.json")

DEFAULT_STRATEGY_CONFIG: dict[str, Any] = {
    "strategy_name": "Threshold Strategy",
    "symbol": "MOCKSTOCK",
    "timeframe": "1 Minute",
    "buy_threshold": float(BUY_THRESHOLD),
    "sell_threshold": float(SELL_THRESHOLD),
    "stop_loss_percent": float(STOP_LOSS_PERCENT),
    "target_percent": float(TARGET_PERCENT),
    "risk_per_trade_percent": float(RISK_PER_TRADE_PERCENT),
    "max_position_size_percent": float(MAX_POSITION_SIZE_PERCENT),
    "enabled": True,
}


def validate_strategy_config(
    strategy_config: dict[str, Any],
) -> tuple[bool, str]:
    """
    Validate strategy configuration values.
    """

    if not isinstance(strategy_config, dict):
        return False, "Strategy configuration must be a dictionary."

    strategy_name = strategy_config.get("strategy_name")

    if not isinstance(strategy_name, str) or not strategy_name.strip():
        return False, "Strategy name is required."

    symbol = strategy_config.get("symbol")

    if not isinstance(symbol, str) or not symbol.strip():
        return False, "Stock symbol is required."

    timeframe = strategy_config.get("timeframe")

    if not isinstance(timeframe, str) or not timeframe.strip():
        return False, "Timeframe is required."

    numeric_fields = {
        "buy_threshold": strategy_config.get("buy_threshold"),
        "sell_threshold": strategy_config.get("sell_threshold"),
        "stop_loss_percent": strategy_config.get(
            "stop_loss_percent"
        ),
        "target_percent": strategy_config.get("target_percent"),
        "risk_per_trade_percent": strategy_config.get(
            "risk_per_trade_percent"
        ),
        "max_position_size_percent": strategy_config.get(
            "max_position_size_percent"
        ),
    }

    for field_name, field_value in numeric_fields.items():
        if not isinstance(field_value, (int, float)):
            return False, f"{field_name} must be numeric."

        numeric_value = float(field_value)

        if not math.isfinite(numeric_value):
            return False, f"{field_name} must be finite."

        if numeric_value <= 0:
            return False, f"{field_name} must be greater than zero."

    buy_threshold = float(strategy_config["buy_threshold"])
    sell_threshold = float(strategy_config["sell_threshold"])

    if sell_threshold >= buy_threshold:
        return (
            False,
            "Sell threshold must be lower than buy threshold.",
        )

    percentage_fields = {
        "stop_loss_percent":
            strategy_config["stop_loss_percent"],
        "target_percent":
            strategy_config["target_percent"],
        "risk_per_trade_percent":
            strategy_config["risk_per_trade_percent"],
        "max_position_size_percent":
            strategy_config["max_position_size_percent"],
    }

    for field_name, field_value in percentage_fields.items():
        if float(field_value) > 100:
            return False, f"{field_name} cannot exceed 100%."

    enabled = strategy_config.get("enabled")

    if not isinstance(enabled, bool):
        return False, "enabled must be True or False."

    return True, "Strategy configuration is valid."


def save_strategy_config(
    strategy_config: dict[str, Any],
) -> tuple[bool, str]:
    """
    Validate and save strategy configuration as JSON.
    """

    is_valid, validation_message = validate_strategy_config(
        strategy_config
    )

    if not is_valid:
        return False, validation_message

    try:
        STRATEGY_CONFIG_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        normalized_config = {
            "strategy_name": strategy_config[
                "strategy_name"
            ].strip(),
            "symbol": strategy_config["symbol"].strip().upper(),
            "timeframe": strategy_config["timeframe"].strip(),
            "buy_threshold": float(
                strategy_config["buy_threshold"]
            ),
            "sell_threshold": float(
                strategy_config["sell_threshold"]
            ),
            "stop_loss_percent": float(
                strategy_config["stop_loss_percent"]
            ),
            "target_percent": float(
                strategy_config["target_percent"]
            ),
            "risk_per_trade_percent": float(
                strategy_config["risk_per_trade_percent"]
            ),
            "max_position_size_percent": float(
                strategy_config["max_position_size_percent"]
            ),
            "enabled": bool(strategy_config["enabled"]),
        }

        with STRATEGY_CONFIG_FILE.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                normalized_config,
                file,
                indent=4,
            )

        return True, "Strategy saved successfully."

    except (OSError, TypeError, ValueError) as error:
        return False, f"Strategy could not be saved: {error}"


def load_strategy_config() -> tuple[dict[str, Any], str]:
    """
    Load saved strategy configuration.

    If no saved file exists, create and return the default strategy.
    """

    if not STRATEGY_CONFIG_FILE.exists():
        saved, message = save_strategy_config(
            DEFAULT_STRATEGY_CONFIG.copy()
        )

        if saved:
            return (
                DEFAULT_STRATEGY_CONFIG.copy(),
                "Default strategy created.",
            )

        return DEFAULT_STRATEGY_CONFIG.copy(), message

    try:
        with STRATEGY_CONFIG_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:
            strategy_config = json.load(file)

        is_valid, validation_message = validate_strategy_config(
            strategy_config
        )

        if not is_valid:
            return (
                DEFAULT_STRATEGY_CONFIG.copy(),
                f"Invalid saved strategy: {validation_message}",
            )

        return strategy_config, "Strategy loaded successfully."

    except (
        OSError,
        json.JSONDecodeError,
        TypeError,
        ValueError,
    ) as error:
        return (
            DEFAULT_STRATEGY_CONFIG.copy(),
            f"Strategy could not be loaded: {error}",
        )