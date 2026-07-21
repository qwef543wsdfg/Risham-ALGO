"""
Sidebar navigation for Risham Algo Terminal.
"""

from textwrap import dedent

import streamlit as st


NAVIGATION_OPTIONS = [
    "📊 Dashboard",
    "📈 Live Trading",
    "🧠 Strategy Builder",
    "💼 Portfolio",
    "📜 Trades",
    "📊 Analytics",
    "⚙️ Settings",
    "ℹ️ About",
]

APPLICATION_VERSION = "V2.0"
TRADING_MODE = "Paper Trading"


def _clean_html(html_content: str) -> str:
    """
    Remove indentation and blank lines from an HTML block.

    This prevents Streamlit Markdown from displaying indented HTML
    as a visible code block.
    """

    cleaned_lines = [
        line.strip()
        for line in dedent(html_content).splitlines()
        if line.strip()
    ]

    return "".join(cleaned_lines)


def _render_sidebar_html(html_content: str) -> None:
    """
    Render trusted HTML inside the Streamlit sidebar.
    """

    st.markdown(
        _clean_html(html_content),
        unsafe_allow_html=True,
    )


def _render_brand() -> None:
    """Render the application branding section."""

    _render_sidebar_html(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-row">
                <div class="sidebar-logo">
                    <span>R</span>
                </div>
                <div class="sidebar-brand-content">
                    <div class="sidebar-title">RISHAM ALGO</div>
                    <div class="sidebar-subtitle">
                        Institutional Trading Terminal
                    </div>
                </div>
            </div>
        </div>
        """
    )


def _render_navigation_heading() -> None:
    """Render the sidebar navigation heading."""

    _render_sidebar_html(
        """
        <div class="sidebar-section-heading">
            TERMINAL
        </div>
        """
    )


def _render_system_status() -> None:
    """Render system and trading-mode information."""

    _render_sidebar_html(
        f"""
        <div class="sidebar-status-card">
            <div class="sidebar-status-header">
                <div class="sidebar-status-title">
                    System Status
                </div>
                <div class="sidebar-version">
                    {APPLICATION_VERSION}
                </div>
            </div>

            <div class="sidebar-status-value">
                <span class="status-dot"></span>
                <span>All Systems Operational</span>
            </div>

            <div class="sidebar-status-divider"></div>

            <div class="sidebar-mode-row">
                <span class="sidebar-mode-label">
                    Trading Mode
                </span>
                <span class="sidebar-mode-value">
                    {TRADING_MODE}
                </span>
            </div>
        </div>
        """
    )


def _render_sidebar_footer() -> None:
    """Render the sidebar footer."""

    _render_sidebar_html(
        """
        <div class="sidebar-footer">
            <div class="sidebar-footer-title">
                Risham Algo Technologies
            </div>
            <div class="sidebar-footer-text">
                Secure · Automated · Data Driven
            </div>
        </div>
        """
    )


def show_sidebar() -> str:
    """
    Render the sidebar and return the selected navigation page.
    """

    with st.sidebar:
        _render_brand()
        _render_navigation_heading()

        selected_page = st.radio(
            "Navigation",
            options=NAVIGATION_OPTIONS,
            label_visibility="collapsed",
            key="sidebar_navigation",
        )

        _render_system_status()
        _render_sidebar_footer()

    return selected_page