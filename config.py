"""
Project configuration settings.

This file stores values that may change in the future.
Keeping them here avoids hardcoding values in multiple files.
"""

import math

# Stock configuration
STOCK_SYMBOL: str = "MOCKSTOCK"

# Mock market configuration
START_PRICE: float = 100.0
PRICE_UPDATE_INTERVAL: int = 2  # seconds

# Trading strategy thresholds
BUY_THRESHOLD: float = 105.0
SELL_THRESHOLD: float = 95.0

# CSV storage path
CSV_FILE_PATH: str = "data/signals.csv"





# Paper trading portfolio configuration
INITIAL_CAPITAL: float = 100_000.0

# Risk management configuration
RISK_PER_TRADE_PERCENT: float = 1.0
MAX_POSITION_SIZE_PERCENT: float = 20.0
STOP_LOSS_PERCENT: float = 2.0
TARGET_PERCENT: float = 4.0

# V2 CSV storage paths
TRADES_FILE_PATH: str = "data/trades.csv"
PORTFOLIO_FILE_PATH: str = "data/portfolio.csv"
PRICE_HISTORY_FILE_PATH: str = "data/price_history.csv"
PRICE_HISTORY_FILE_PATH: str = "data/price_history.csv"



def validate_config() -> tuple[bool, str]:
    """
    Validate project configuration values.

    Returns:
        A tuple containing:
        - True and a success message when configuration is valid.
        - False and an error message when configuration is invalid.
    """
    if not isinstance(STOCK_SYMBOL, str) or not STOCK_SYMBOL.strip():
        return False, "STOCK_SYMBOL must contain a valid stock name."

    if not isinstance(START_PRICE, (int, float)):
        return False, "START_PRICE must be numeric."

    if not math.isfinite(float(START_PRICE)) or START_PRICE <= 0:
        return False, "START_PRICE must be positive and finite."

    if not isinstance(BUY_THRESHOLD, (int, float)):
        return False, "BUY_THRESHOLD must be numeric."

    if not isinstance(SELL_THRESHOLD, (int, float)):
        return False, "SELL_THRESHOLD must be numeric."

    if not math.isfinite(float(BUY_THRESHOLD)):
        return False, "BUY_THRESHOLD must be finite."

    if not math.isfinite(float(SELL_THRESHOLD)):
        return False, "SELL_THRESHOLD must be finite."

    if SELL_THRESHOLD >= BUY_THRESHOLD:
        return False, "SELL_THRESHOLD must be lower than BUY_THRESHOLD."

    if not isinstance(PRICE_UPDATE_INTERVAL, int):
        return False, "PRICE_UPDATE_INTERVAL must be an integer."

    if PRICE_UPDATE_INTERVAL <= 0:
        return False, "PRICE_UPDATE_INTERVAL must be greater than zero."

  






    if not isinstance(CSV_FILE_PATH, str) or not CSV_FILE_PATH.strip():
        return False, "CSV_FILE_PATH must contain a valid file path."

    if (
        isinstance(INITIAL_CAPITAL, bool)
        or not isinstance(INITIAL_CAPITAL, (int, float))
    ):
        return False, "INITIAL_CAPITAL must be numeric."

    if not math.isfinite(float(INITIAL_CAPITAL)):
      return False, "INITIAL_CAPITAL must be finite."

    if INITIAL_CAPITAL <= 0:
      return False, "INITIAL_CAPITAL must be greater than zero."
    percentage_settings = {
        "RISK_PER_TRADE_PERCENT": RISK_PER_TRADE_PERCENT,
        "MAX_POSITION_SIZE_PERCENT": MAX_POSITION_SIZE_PERCENT,
        "STOP_LOSS_PERCENT": STOP_LOSS_PERCENT,
        "TARGET_PERCENT": TARGET_PERCENT,
    }

    for setting_name, setting_value in percentage_settings.items():
        if (
            isinstance(setting_value, bool)
            or not isinstance(setting_value, (int, float))
        ):
            return False, f"{setting_name} must be numeric."

        if not math.isfinite(float(setting_value)):
            return False, f"{setting_name} must be finite."

        if setting_value <= 0:
            return False, f"{setting_name} must be greater than zero."

        if setting_value > 100:
            return False, f"{setting_name} cannot exceed 100."

    file_path_settings = {
        "TRADES_FILE_PATH": TRADES_FILE_PATH,
        "PORTFOLIO_FILE_PATH": PORTFOLIO_FILE_PATH,
        "PRICE_HISTORY_FILE_PATH": PRICE_HISTORY_FILE_PATH,
    }

    for setting_name, setting_value in file_path_settings.items():
        if not isinstance(setting_value, str) or not setting_value.strip():
            return False, f"{setting_name} must contain a valid file path."

    return True, "Configuration is valid."