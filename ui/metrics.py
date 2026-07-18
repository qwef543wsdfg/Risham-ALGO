"""
Reusable metric-card components for the Algo Trading dashboard.
"""

from html import escape

import streamlit as st


def show_metric_card(
    label: str,
    value: str,
    helper: str = "",
) -> None:
    """
    Display one custom dashboard metric card.

    Args:
        label: Small heading shown above the main value.
        value: Main metric value.
        helper: Optional supporting text.
    """

    safe_label = escape(str(label))
    safe_value = escape(str(value))
    safe_helper = escape(str(helper))

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{safe_label}</div>
            <div class="metric-value">{safe_value}</div>
            <div class="metric-helper">{safe_helper}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_top_metrics(
    current_price: float,
    signal: str,
    quantity: int,
    cash: float,
    total_equity: float,
    total_pnl: float,
) -> None:
    """Display the dashboard's main trading metrics."""

    columns = st.columns(6)

    metric_values = (
        (
            "Current Price",
            f"₹{current_price:,.2f}",
            "Latest mock-market price",
        ),
        (
            "Signal",
            signal,
            "Strategy decision",
        ),
        (
            "Position",
            str(quantity),
            "Open share quantity",
        ),
        (
            "Available Cash",
            f"₹{cash:,.2f}",
            "Unused account balance",
        ),
        (
            "Total Equity",
            f"₹{total_equity:,.2f}",
            "Cash plus position value",
        ),
        (
            "Total PnL",
            f"₹{total_pnl:,.2f}",
            "Realized plus unrealized",
        ),
    )

    for column, metric in zip(columns, metric_values):
        with column:
            show_metric_card(*metric)