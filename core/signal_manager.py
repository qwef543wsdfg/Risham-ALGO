"""
Create, write, and read the CSV signal-history file safely.
"""

import csv
import math
from datetime import datetime
from pathlib import Path

from config import CSV_FILE_PATH


CSV_HEADERS: list[str] = ["timestamp", "stock", "price", "signal"]
VALID_SIGNALS: set[str] = {"BUY", "SELL", "HOLD"}


def ensure_csv_exists() -> bool:
    """
    Create the data folder and CSV file if they do not already exist.

    Returns True when the CSV file is ready to use.
    Returns False when a file-related error occurs.
    """
    csv_path = Path(CSV_FILE_PATH)

    try:
        csv_path.parent.mkdir(parents=True, exist_ok=True)

        if not csv_path.exists() or csv_path.stat().st_size == 0:
            with csv_path.open(
                mode="w",
                newline="",
                encoding="utf-8",
            ) as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(CSV_HEADERS)

        return True

    except (OSError, PermissionError) as error:
        print(f"Could not prepare CSV file: {error}")
        return False


def save_signal(stock: str, price: float, signal: str) -> bool:
    """
    Validate and save one signal record to the CSV file.

    Returns True when the record is saved successfully.
    Returns False when validation or file writing fails.
    """
    if not isinstance(stock, str) or not stock.strip():
        print("Could not save signal: stock name is invalid.")
        return False

    if not isinstance(price, (int, float)):
        print("Could not save signal: price must be numeric.")
        return False

    numeric_price: float = float(price)

    if not math.isfinite(numeric_price) or numeric_price <= 0:
        print("Could not save signal: price must be positive and finite.")
        return False

    if not isinstance(signal, str):
        print("Could not save signal: signal must be text.")
        return False

    normalized_signal: str = signal.strip().upper()

    if normalized_signal not in VALID_SIGNALS:
        print("Could not save signal: signal must be BUY, SELL, or HOLD.")
        return False

    if not ensure_csv_exists():
        return False

    csv_path = Path(CSV_FILE_PATH)
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with csv_path.open(
            mode="a",
            newline="",
            encoding="utf-8",
        ) as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                [
                    timestamp,
                    stock.strip().upper(),
                    f"{numeric_price:.2f}",
                    normalized_signal,
                ]
            )

        return True

    except (OSError, PermissionError, csv.Error) as error:
        print(f"Could not save signal: {error}")
        return False
    



    

def is_duplicate_signal(stock: str, signal: str) -> bool:
    """
    Return True when the latest saved signal is the same
    for the supplied stock.
    """
    if not isinstance(stock, str) or not stock.strip():
        return False

    if not isinstance(signal, str) or not signal.strip():
        return False

    recent_records = read_recent_signals(1)

    if not recent_records:
        return False

    latest_record = recent_records[-1]

    latest_stock = latest_record.get("stock", "").strip().upper()
    latest_signal = latest_record.get("signal", "").strip().upper()

    current_stock = stock.strip().upper()
    current_signal = signal.strip().upper()

    return (
        latest_stock == current_stock
        and latest_signal == current_signal
    )



def read_recent_signals(limit: int = 10) -> list[dict[str, str]]:
    """
    Read and return the most recent signal records.

    An empty list is returned when no records exist or reading fails.
    """
    if not isinstance(limit, int) or limit <= 0:
        return []

    if not ensure_csv_exists():
        return []

    csv_path = Path(CSV_FILE_PATH)

    try:
        with csv_path.open(
            mode="r",
            newline="",
            encoding="utf-8",
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            records = list(reader)

        return records[-limit:]

    except (OSError, PermissionError, csv.Error) as error:
        print(f"Could not read CSV file: {error}")
        return []