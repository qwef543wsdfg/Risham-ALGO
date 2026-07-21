"""Table helpers for the trading dashboard."""

from html import escape
from textwrap import dedent

import streamlit as st


def _clean_html(html: str) -> str:
    """
    Remove indentation so Streamlit renders HTML correctly.
    """

    cleaned_html = dedent(html).strip()

    return "".join(
        line.strip()
        for line in cleaned_html.splitlines()
        if line.strip()
    )


def _get_signal_class(signal: str) -> str:
    """
    Return the visual class for a trading signal.
    """

    normalized_signal = signal.strip().upper()

    if normalized_signal == "BUY":
        return "signal-buy"

    if normalized_signal == "SELL":
        return "signal-sell"

    return "signal-hold"


def _format_price(price: str) -> str:
    """
    Format a valid numeric price as currency.
    """

    try:
        return f"₹{float(price):,.2f}"
    except (TypeError, ValueError):
        return "n/a"


def show_signal_table(signals: list[dict[str, str]]) -> None:
    """
    Display recent trading signals in a premium HTML table.
    """

    if not signals:
        empty_state_html = _clean_html(
            """
            <div class="signal-panel">
                <div class="signal-panel-header">
                    <div>
                        <div class="panel-eyebrow">Market Activity</div>
                        <div class="panel-title">Recent Signals</div>
                    </div>
                    <div class="table-count-badge">0 Signals</div>
                </div>

                <div class="table-empty-state">
                    <div class="table-empty-icon">—</div>
                    <div class="table-empty-title">
                        No signal history yet
                    </div>
                    <div class="table-empty-text">
                        New BUY, SELL or HOLD signals will appear here.
                    </div>
                </div>
            </div>
            """
        )

        st.markdown(
            empty_state_html,
            unsafe_allow_html=True,
        )
        return

    table_rows: list[str] = []

    for record in signals:
        timestamp = escape(
            str(record.get("timestamp", "n/a"))
        )

        signal = str(
            record.get("signal", "HOLD")
        ).strip().upper()

        safe_signal = escape(signal)
        signal_class = _get_signal_class(signal)

        price = _format_price(
            str(record.get("price", "n/a"))
        )

        table_rows.append(
            f"""
            <tr>
                <td class="signal-time">{timestamp}</td>
                <td>
                    <span class="signal-badge {signal_class}">
                        <span class="signal-badge-dot"></span>
                        {safe_signal}
                    </span>
                </td>
                <td class="signal-price">{price}</td>
            </tr>
            """
        )

    rows_html = "".join(table_rows)

    table_html = _clean_html(
        f"""
        <div class="signal-panel">
            <div class="signal-panel-header">
                <div>
                    <div class="panel-eyebrow">Market Activity</div>
                    <div class="panel-title">Recent Signals</div>
                </div>

                <div class="table-count-badge">
                    {len(signals)} Signals
                </div>
            </div>

            <div class="signal-table-wrapper">
                <table class="signal-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Signal</th>
                            <th class="table-price-heading">Price</th>
                        </tr>
                    </thead>

                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>

            <div class="signal-panel-footer">
                <span>Latest strategy decisions</span>

                <span class="table-live-status">
                    <span class="table-live-dot"></span>
                    Live
                </span>
            </div>
        </div>
        """
    )

    st.markdown(
        table_html,
        unsafe_allow_html=True,
    )