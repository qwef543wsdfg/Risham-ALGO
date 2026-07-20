"""
Main Streamlit dashboard for Algo Trading V2.
"""

from datetime import datetime
from ui.strategy_page import show_strategy_page
import streamlit as st

from config import PRICE_UPDATE_INTERVAL, STOCK_SYMBOL
from core.market_data import generate_mock_price
from core.pnl import calculate_portfolio_metrics
from core.portfolio import load_portfolio
from core.price_history import read_price_history, save_price
from core.signal_manager import (
    is_duplicate_signal,
    read_recent_signals,
    save_signal,
)
from core.strategy import generate_signal
from core.trade_engine import execute_signal
from ui.charts import show_price_chart
from ui.metrics import show_top_metrics
from ui.tables import show_signal_table
from ui.theme import apply_theme


def get_chart_prices(limit: int = 50) -> list[float]:
    """
    Read saved price-history rows and return valid numeric prices.
    """

    price_rows = read_price_history(limit)
    prices: list[float] = []

    for row in price_rows:
        try:
            price = float(row["price"])

            if price > 0:
                prices.append(price)

        except (KeyError, TypeError, ValueError):
            continue

    return prices



def show_dashboard() -> None:
    """
    Render dashboard navigation and the selected page.
    """

    apply_theme()
    show_dashboard_header()

    selected_page = st.radio(
        "Main Navigation",
        options=[
            "Dashboard",
            "Strategy Builder",
        ],
        horizontal=True,
        label_visibility="collapsed",
        key="main_navigation",
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    if selected_page == "Dashboard":
        st.info(
            "Mock-market paper trading environment. "
            "No real broker orders are placed."
        )

        show_live_signal()
        return

    show_strategy_page()


@st.fragment(run_every=PRICE_UPDATE_INTERVAL)
def show_live_signal() -> None:
    """Generate and display the refreshed paper-trading dashboard."""

    price: float = generate_mock_price()
    signal: str = generate_signal(price)
    update_time: str = datetime.now().strftime("%I:%M:%S %p")

    # Save every generated price for the chart.
    price_saved: bool = save_price(price)

    duplicate: bool = is_duplicate_signal(
        STOCK_SYMBOL,
        signal,
    )

    trade_message = ""
    trade_success: bool | None = None

    if not duplicate:
        signal_saved: bool = save_signal(
            STOCK_SYMBOL,
            price,
            signal,
        )

        if signal_saved:
            (
                trade_success,
                _,
                trade_message,
            ) = execute_signal(
                signal=signal,
                price=price,
            )
    else:
        signal_saved = False

    portfolio, portfolio_message = load_portfolio()

    if portfolio is None:
        st.error(portfolio_message)
        return

    try:
        metrics = calculate_portfolio_metrics(
            portfolio=portfolio,
            current_price=price,
        )
    except (KeyError, TypeError, ValueError) as error:
        st.error(
            f"Portfolio metrics could not be calculated: {error}"
        )
        return

    realized_pnl = float(
        portfolio.get("realized_pnl", 0.0)
    )

    unrealized_pnl = float(
        metrics.get("unrealized_pnl", 0.0)
    )

    total_pnl = realized_pnl + unrealized_pnl

    st.subheader("Live Signal")

    show_top_metrics(
        current_price=price,
        signal=signal,
        quantity=int(portfolio["quantity"]),
        cash=float(metrics["cash"]),
        total_equity=float(metrics["total_equity"]),
        total_pnl=total_pnl,
    )

    st.caption(
        f"Last updated: {update_time} · "
        f"Refresh interval: {PRICE_UPDATE_INTERVAL} seconds"
    )

    if duplicate:
        st.info(
            "Signal unchanged. Duplicate signal was not saved."
        )
    elif signal_saved:
        st.success("New signal saved successfully.")
    else:
        st.error("Signal could not be saved.")

    if trade_success is True:
        st.success(trade_message)
    elif trade_success is False:
        st.warning(trade_message)

    if not price_saved:
        st.warning("Current price could not be saved to history.")

    st.markdown("<hr/>", unsafe_allow_html=True)

    left_column, right_column = st.columns(
        [1.5, 1.0],
        gap="medium",
    )

    with left_column:
        price_history = get_chart_prices(50)
        show_price_chart(price_history)

    with right_column:
        recent_signals = read_recent_signals(8)
        show_signal_table(recent_signals)


def show_dashboard_header() -> None:
    """Render the dashboard header used by pages."""

    st.markdown(
        f"""
<div class="algo-header">
    <div>
        <div class="algo-title">📈 Risham Algo V2</div>
        <div class="algo-subtitle">
            Paper Trading Dashboard · {STOCK_SYMBOL}
        </div>
    </div>

    <div class="live-badge">
        <span class="live-dot"></span>
        SYSTEM LIVE
    </div>
</div>
""",
        unsafe_allow_html=True,
    )