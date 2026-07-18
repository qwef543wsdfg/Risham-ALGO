"""
Visual theme and custom CSS for Algo Trading V2.
"""

import streamlit as st


def apply_theme() -> None:
    """Apply the custom dashboard styling."""

    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(
                    circle at top left,
                    rgba(30, 64, 175, 0.15),
                    transparent 30%
                ),
                #070b14;
            color: #f8fafc;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            background-color: #0b1220;
            border-right: 1px solid #1e293b;
        }

        .block-container {
            max-width: 1600px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .algo-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.2rem;
        }

        .algo-title {
            font-size: 2rem;
            font-weight: 750;
            letter-spacing: -0.04em;
            color: #f8fafc;
        }

        .algo-subtitle {
            margin-top: 0.25rem;
            color: #94a3b8;
            font-size: 0.9rem;
        }

        .live-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            border: 1px solid rgba(34, 197, 94, 0.35);
            background-color: rgba(34, 197, 94, 0.1);
            color: #86efac;
            font-size: 0.78rem;
            font-weight: 700;
        }

        .live-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #22c55e;
            box-shadow: 0 0 10px rgba(34, 197, 94, 0.9);
        }

        .metric-card {
            min-height: 118px;
            padding: 1rem 1.1rem;
            border-radius: 16px;
            background: linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.95),
                rgba(9, 15, 28, 0.96)
            );
            border: 1px solid #1e293b;
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.22);
        }

        .metric-label {
            color: #94a3b8;
            font-size: 0.78rem;
            font-weight: 650;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .metric-value {
            margin-top: 0.55rem;
            color: #f8fafc;
            font-size: 1.55rem;
            font-weight: 760;
        }

        .metric-helper {
            margin-top: 0.35rem;
            color: #64748b;
            font-size: 0.76rem;
        }

        .panel-card {
            padding: 1rem;
            border-radius: 16px;
            background-color: rgba(11, 18, 32, 0.94);
            border: 1px solid #1e293b;
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.18);
        }

        .panel-title {
            margin-bottom: 0.8rem;
            color: #e2e8f0;
            font-size: 1rem;
            font-weight: 700;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #1e293b;
            border-radius: 14px;
            overflow: hidden;
        }

        hr {
            border-color: #1e293b !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )