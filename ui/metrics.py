"""
Reusable metric-card components for the Algo Trading dashboard.
"""

from html import escape
from textwrap import dedent

import streamlit as st


VALID_TONES = {
    "default",
    "primary",
    "success",
    "danger",
    "warning",
}


def _clean_html(html_content: str) -> str:
    """
    Convert multiline HTML into compact markup.

    This prevents Streamlit from displaying indented HTML
    as a visible code block.
    """

    return "".join(
        line.strip()
        for line in dedent(html_content).splitlines()
        if line.strip()
    )


def _get_signal_tone(signal: str) -> str:
    """
    Return the visual tone associated with a trading signal.
    """

    normalized_signal = str(signal).strip().upper()

    if normalized_signal == "BUY":
        return "success"

    if normalized_signal == "SELL":
        return "danger"

    return "warning"


def _get_pnl_tone(total_pnl: float) -> str:
    """
    Return the visual tone associated with total PnL.
    """

    if total_pnl > 0:
        return "success"

    if total_pnl < 0:
        return "danger"

    return "default"


def _get_position_value(quantity: int) -> str:
    """
    Return a readable position label.
    """

    if quantity > 0:
        return "LONG"

    return "FLAT"


def show_metric_card(
    label: str,
    value: str,
    helper: str = "",
    icon: str = "●",
    tone: str = "default",
) -> None:
    """
    Display one premium dashboard metric card.

    Args:
        label: Small heading shown above the main value.
        value: Main metric value.
        helper: Supporting information shown below the value.
        icon: Compact visual identifier for the metric.
        tone: Visual state used for the value and icon.
    """

    safe_label = escape(str(label))
    safe_value = escape(str(value))
    safe_helper = escape(str(helper))
    safe_icon = escape(str(icon))

    safe_tone = (
        tone
        if tone in VALID_TONES
        else "default"
    )

    metric_html = _clean_html(
        f"""
        <div class="metric-card metric-card-{safe_tone}">
            <div class="metric-card-top">
                <div class="metric-label">
                    {safe_label}
                </div>

                <div class="metric-icon metric-icon-{safe_tone}">
                    {safe_icon}
                </div>
            </div>

            <div class="metric-value metric-value-{safe_tone}">
                {safe_value}
            </div>

            <div class="metric-helper">
                {safe_helper}
            </div>
        </div>
        """
    )

    st.markdown(
        metric_html,
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
    """
    Display the dashboard's main trading metrics.
    """

    normalized_signal = str(signal).strip().upper()
    signal_tone = _get_signal_tone(normalized_signal)
    pnl_tone = _get_pnl_tone(total_pnl)
    position_value = _get_position_value(quantity)

    columns = st.columns(
        6,
        gap="small",
    )

    metric_values = (
        {
            "label": "Current Price",
            "value": f"₹{current_price:,.2f}",
            "helper": "Latest mock-market price",
            "icon": "₹",
            "tone": "primary",
        },
        {
            "label": "Current Signal",
            "value": normalized_signal,
            "helper": "Active strategy decision",
            "icon": "↗",
            "tone": signal_tone,
        },
        {
            "label": "Position",
            "value": position_value,
            "helper": f"Quantity: {quantity:,} shares",
            "icon": "P",
            "tone": (
                "success"
                if quantity > 0
                else "default"
            ),
        },
        {
            "label": "Available Cash",
            "value": f"₹{cash:,.2f}",
            "helper": "Unused account balance",
            "icon": "C",
            "tone": "default",
        },
        {
            "label": "Total Equity",
            "value": f"₹{total_equity:,.2f}",
            "helper": "Cash plus position value",
            "icon": "E",
            "tone": "primary",
        },
        {
            "label": "Total P&L",
            "value": f"₹{total_pnl:,.2f}",
            "helper": "Realized plus unrealized",
            "icon": "₹",
            "tone": pnl_tone,
        },
    )

    for column, metric in zip(
        columns,
        metric_values,
    ):
        with column:
            show_metric_card(**metric)