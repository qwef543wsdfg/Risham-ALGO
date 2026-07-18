"""Table helpers for the trading dashboard."""

import streamlit as st


def show_signal_table(signals: list[dict[str, str]]) -> None:
    """Display a compact table of recent signals."""

    st.markdown(
        '<div class="panel-card"><div class="panel-title">Recent Signals</div></div>',
        unsafe_allow_html=True,
    )

    if not signals:
        st.caption("No signal history yet.")
        return

    rows = [
        {
            "Time": record.get("timestamp", "n/a"),
            "Signal": record.get("signal", "HOLD"),
            "Price": record.get("price", "n/a"),
        }
        for record in signals
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)
