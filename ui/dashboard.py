"""
Main Streamlit dashboard for Algo Trading V2.
"""

from datetime import datetime
from textwrap import dedent

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
from ui.sidebar import show_sidebar
from ui.strategy_page import show_strategy_page
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
    Render the selected application page.
    """

    apply_theme()

    selected_page = show_sidebar()

    show_dashboard_header()

    if selected_page == "📊 Dashboard":
        show_live_signal()
        return

    if selected_page == "📈 Live Trading":
        st.title("Live Trading")

        st.info(
            "Live trading controls will be added in the next phase."
        )
        return

    if selected_page == "🧠 Strategy Builder":
        show_strategy_page()
        return

    if selected_page == "💼 Portfolio":
        st.title("Portfolio")

        st.info(
            "Portfolio information will be added in the next phase."
        )
        return

    if selected_page == "📜 Trades":
        st.title("Trade History")

        st.info(
            "Complete trade history will be added in the next phase."
        )
        return

    if selected_page == "📊 Analytics":
        st.title("Analytics")

        st.info(
            "Strategy and portfolio analytics will be added later."
        )
        return

    if selected_page == "⚙️ Settings":
        st.title("Settings")

        st.info(
            "Application settings will be added later."
        )
        return

    st.title("About Risham Algo")

    st.write(
        "Risham Algo V2 is a mock-market paper-trading "
        "and strategy-testing application."
    )


@st.fragment(run_every=PRICE_UPDATE_INTERVAL)
def show_live_signal() -> None:
    """
    Generate and display the refreshed paper-trading dashboard.
    """

    price: float = generate_mock_price()
    signal: str = generate_signal(price)

    update_time: str = datetime.now().strftime(
        "%I:%M:%S %p"
    )

    price_saved: bool = save_price(price)

    duplicate: bool = is_duplicate_signal(
        STOCK_SYMBOL,
        signal,
    )

    signal_saved = False
    trade_message = ""
    trade_success: bool | None = None

    if not duplicate:
        signal_saved = save_signal(
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

    try:
        quantity = int(
            portfolio.get("quantity", 0)
        )

        realized_pnl = float(
            portfolio.get("realized_pnl", 0.0)
        )

        cash = float(
            metrics.get("cash", 0.0)
        )

        total_equity = float(
            metrics.get("total_equity", 0.0)
        )

        unrealized_pnl = float(
            metrics.get("unrealized_pnl", 0.0)
        )

    except (TypeError, ValueError) as error:
        st.error(
            f"Portfolio values are invalid: {error}"
        )
        return

    total_pnl = realized_pnl + unrealized_pnl

    show_top_metrics(
        current_price=price,
        signal=signal,
        quantity=quantity,
        cash=cash,
        total_equity=total_equity,
        total_pnl=total_pnl,
    )

    status_message = get_status_message(
        duplicate=duplicate,
        signal_saved=signal_saved,
        trade_success=trade_success,
        trade_message=trade_message,
    )

    st.caption(
        f"Last updated: {update_time} · "
        f"Refresh interval: {PRICE_UPDATE_INTERVAL} seconds · "
        f"{status_message}"
    )

    if not price_saved:
        st.warning(
            "Current price could not be saved to history."
        )

    st.markdown(
        "<hr/>",
        unsafe_allow_html=True,
    )

    left_column, right_column = st.columns(
        [1.5, 1.0],
        gap="medium",
    )

    with left_column:
        price_history = get_chart_prices(
            limit=50
        )

        show_price_chart(price_history)

    with right_column:
        recent_signals = read_recent_signals(
            8
        )

        show_signal_table(recent_signals)


def get_status_message(
    duplicate: bool,
    signal_saved: bool,
    trade_success: bool | None,
    trade_message: str,
) -> str:
    """
    Return a short dashboard status message.
    """

    if trade_message:
        return trade_message

    if trade_success is True:
        return "Trade executed successfully"

    if trade_success is False:
        return "Trade was not executed"

    if duplicate:
        return "Signal unchanged"

    if signal_saved:
        return "New signal saved"

    return "Signal could not be saved"


def show_dashboard_header() -> None:
    """
    Render the professional dashboard header.
    """

    current_time = datetime.now().strftime(
        "%I:%M:%S %p"
    )

    header_html = dedent(
        f"""
        <div class="dashboard-header">
            <div class="dashboard-header-left">
                <div class="dashboard-brand-row">
                    <div class="dashboard-logo">R</div>
                    <div class="dashboard-heading-content">
                        <div class="dashboard-title">
                            RISHAM ALGO TERMINAL
                        </div>
                        <div class="dashboard-subtitle">
                            Institutional Paper Trading Platform
                        </div>
                    </div>
                </div>
            </div>
            <div class="dashboard-header-right">
                <div class="running-status">
                    <span class="running-dot"></span>
                    <span>System Running</span>
                </div>
                <div class="mode-badge">
                    Paper Trading
                </div>
                <div class="last-updated">
                    {current_time}
                </div>
            </div>
        </div>
        """
    ).strip()

    compact_header_html = "".join(
        line.strip()
        for line in header_html.splitlines()
        if line.strip()
    )

    st.markdown(
        compact_header_html,
        unsafe_allow_html=True,
    )