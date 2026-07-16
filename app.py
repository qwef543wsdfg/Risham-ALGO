"""
Streamlit dashboard for the Algo Trading V2 project.
"""

from datetime import datetime

import streamlit as st
from price_history import save_price

from config import (
    PRICE_UPDATE_INTERVAL,
    STOCK_SYMBOL,
    validate_config,
)
from core.market_data import generate_mock_price
from signal_manager import (
    is_duplicate_signal,
    read_recent_signals,
    save_signal,
)
from core.strategy import generate_signal

from pnl import calculate_portfolio_metrics
from portfolio import load_portfolio
from trade_engine import execute_signal

st.set_page_config(
    page_title="Algo Trading V2",
    page_icon="📈",
    layout="wide",
)


@st.fragment(run_every=PRICE_UPDATE_INTERVAL)
def show_live_signal() -> None:

    """Generate, save, and display the latest mock trading signal."""

    price: float = generate_mock_price()
    save_price(price)
    signal: str = generate_signal(price)
    update_time: str = datetime.now().strftime("%I:%M:%S %p")

    trade_success: bool | None = None
    trade_details: dict[str, object] | None = None
    trade_message: str = ""

    duplicate: bool = is_duplicate_signal(STOCK_SYMBOL, signal)

    if duplicate:
        save_status: str = "duplicate"
        saved = False
    else:
        saved: bool = save_signal(STOCK_SYMBOL, price, signal)

    if saved:
        save_status = "saved"
        (trade_success, trade_details, trade_message) = execute_signal(
            signal=signal, price=price
        )
    else:
        # Either duplicate or failed to save
        if 'save_status' not in locals():
            save_status = "error"
    price_column, signal_column, time_column = st.columns(3)

    with price_column:
        st.metric(
            label="Current Mock Price",
            value=f"₹{price:.2f}",
        )

    with signal_column:
        st.metric(
            label="Current Signal",
            value=signal,
        )

    with time_column:
        st.metric(
            label="Last Updated",
            value=update_time,
        )

    if save_status == "saved":
        st.success("New signal saved successfully.")

    elif save_status == "duplicate":
        st.info(
            "Signal has not changed, so no duplicate row was saved."
        )

    else:
        st.error("Signal could not be saved.")
    if trade_success is True:
        if trade_details is None:
            st.info(trade_message)
        else:
            st.success(trade_message)

    elif trade_success is False:
        st.warning(trade_message)

    st.divider()
    st.subheader("💼 Paper Trading Portfolio")

    portfolio, portfolio_message = load_portfolio()

    if portfolio is None:
        st.error(portfolio_message)

    else:
        try:
            portfolio_metrics = calculate_portfolio_metrics(
                portfolio=portfolio,
                current_price=price,
            )

            cash_column, quantity_column, position_column = st.columns(3)

            with cash_column:
                st.metric(
                    label="Available Cash",
                    value=f"₹{portfolio_metrics['cash']:,.2f}",
                )

            with quantity_column:
                st.metric(
                    label="Current Quantity",
                    value=int(portfolio["quantity"]),
                )

            with position_column:
                st.metric(
                    label="Position Value",
                    value=(
                        f"₹{portfolio_metrics['position_value']:,.2f}"
                    ),
                )

            pnl_column, equity_column, return_column = st.columns(3)

            with pnl_column:
                st.metric(
                    label="Unrealized PnL",
                    value=(
                        f"₹{portfolio_metrics['unrealized_pnl']:,.2f}"
                    ),
                )

            with equity_column:
                st.metric(
                    label="Total Equity",
                    value=(
                        f"₹{portfolio_metrics['total_equity']:,.2f}"
                    ),
                )

            with return_column:
                st.metric(
                    label="Account Return",
                    value=(
                        f"{portfolio_metrics['return_percent']:.2f}%"
                    ),
                )

            st.caption(
                "Average entry price: "
                f"₹{float(portfolio['average_price']):,.2f} | "
                "Realized PnL: "
                f"₹{float(portfolio['realized_pnl']):,.2f}"
            )

        except (KeyError, TypeError, ValueError) as error:
            st.error(
                f"Portfolio metrics could not be calculated: {error}"
            )

    st.divider()
    st.subheader("📜 Recent Signal History")

    history: list[dict[str, str]] = read_recent_signals(10)

    if history:
        st.dataframe(
            history[::-1],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No signal history available.")
def main() -> None:
    """Display the dashboard and live signal section."""
    st.title("📈 Risham Algo ")

    st.write(
    "A mock-data paper-trading dashboard with risk management, "
    "portfolio tracking, and PnL calculations."
)
    st.info(
    "This Algo project uses mock market data and simulated paper "
    "trades. It does not connect to a broker or place real orders."
)

    config_is_valid, config_message = validate_config()

    if not config_is_valid:
        st.error(f"Configuration error: {config_message}")
        st.stop()

    st.subheader(f"Stock: {STOCK_SYMBOL}")

    show_live_signal()


if __name__ == "__main__":
    main()