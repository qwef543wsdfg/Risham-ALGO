"""
Store and read mock price history.
"""

import csv
from datetime import datetime
from pathlib import Path

from config import PRICE_HISTORY_FILE_PATH


PRICE_FIELDS = [
    "timestamp",
    "price",
]


def save_price(
    price: float,
) -> bool:
    """
    Save one market price.
    """

    try:

        path = Path(PRICE_HISTORY_FILE_PATH)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        write_header = (
            not path.exists()
            or path.stat().st_size == 0
        )

        with path.open(
            "a",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=PRICE_FIELDS,
            )

            if write_header:
                writer.writeheader()

            writer.writerow(
                {
                    "timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "price": round(price, 2),
                }
            )

        return True

    except Exception:

        return False
    

def read_price_history(
    limit: int = 100,
) -> list[dict[str, str]]:
    """
    Return recent prices.
    """

    path = Path(
        PRICE_HISTORY_FILE_PATH
    )

    if not path.exists():
        return []

    try:

        with path.open(
            "r",
            newline="",
            encoding="utf-8",
        ) as file:

            reader = csv.DictReader(file)

            rows = list(reader)

        return rows[-limit:]

    except Exception:

        return []