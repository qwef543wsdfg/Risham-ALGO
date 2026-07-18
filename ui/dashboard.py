"""
Main dashboard layout for Algo Trading V2.
"""

import streamlit as st

from config import STOCK_SYMBOL
from ui.theme import apply_theme


def show_dashboard_header() -> None:
    """Display the main application header."""

    st.markdown(
        f"""
        <div class="algo-header">
            <div>
                <div class="algo-title">Risham Algo V2</div>
                <div class="algo-subtitle">
                    Paper trading dashboard · {STOCK_SYMBOL}
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


def show_dashboard() -> None:
    """Render the primary dashboard shell."""

    apply_theme()
    show_dashboard_header()

    st.info(
        "Dashboard UI is connected. Live trading components "
        "will be integrated in the next step."
    )