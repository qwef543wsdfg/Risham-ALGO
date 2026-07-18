"""
Streamlit entry point for Algo Trading V2.
"""

import streamlit as st

from config import validate_config
from ui.dashboard import show_dashboard


st.set_page_config(
    page_title="Algo Trading V2",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    """Validate configuration and render the dashboard."""

    config_is_valid, config_message = validate_config()

    if not config_is_valid:
        st.error(f"Configuration error: {config_message}")
        st.stop()

    show_dashboard()


if __name__ == "__main__":
    main()