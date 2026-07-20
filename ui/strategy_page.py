"""
Dashboard page for creating and managing trading strategies.
"""

from typing import Any

import streamlit as st

from core.strategy_config import (
    load_strategy_config,
    save_strategy_config,
)


TIMEFRAME_OPTIONS = [
    "1 Minute",
    "3 Minutes",
    "5 Minutes",
    "15 Minutes",
    "30 Minutes",
    "1 Hour",
    "1 Day",
]


def change_strategy_status(
    strategy_config: dict[str, Any],
    enabled: bool,
) -> None:
    """
    Enable or disable the currently saved strategy.
    """

    updated_config = strategy_config.copy()
    updated_config["enabled"] = enabled

    success, message = save_strategy_config(
        updated_config
    )

    if success:
        if enabled:
            st.success("Strategy started successfully.")
        else:
            st.warning("Strategy stopped successfully.")

        st.rerun()

    st.error(message)


def show_strategy_status(
    strategy_config: dict[str, Any],
) -> None:
    """
    Display the current strategy status and summary.
    """

    enabled = bool(
        strategy_config.get("enabled", False)
    )

    status_text = (
        "ACTIVE"
        if enabled
        else "STOPPED"
    )

    status_icon = (
        "🟢"
        if enabled
        else "🔴"
    )

    st.markdown(
        f"""
<div class="panel-card">
    <div class="panel-title">
        {status_icon} Strategy Status: {status_text}
    </div>
    <p>
        <strong>Strategy:</strong>
        {strategy_config.get("strategy_name", "Unknown")}
    </p>
    <p>
        <strong>Symbol:</strong>
        {strategy_config.get("symbol", "Unknown")}
        &nbsp; · &nbsp;
        <strong>Timeframe:</strong>
        {strategy_config.get("timeframe", "Unknown")}
    </p>
</div>
""",
        unsafe_allow_html=True,
    )


def show_strategy_form(
    strategy_config: dict[str, Any],
) -> None:
    """
    Display the strategy-builder form.
    """

    st.subheader("Strategy Builder")

    st.caption(
        "Configure the trading rules used by the paper-trading engine."
    )

    with st.form(
        key="strategy_builder_form",
        clear_on_submit=False,
    ):
        st.markdown("### Basic Information")

        basic_left, basic_right = st.columns(2)

        with basic_left:
            strategy_name = st.text_input(
                "Strategy Name",
                value=str(
                    strategy_config.get(
                        "strategy_name",
                        "Threshold Strategy",
                    )
                ),
                placeholder="Example: Breakout Strategy",
            )

            symbol = st.text_input(
                "Stock Symbol",
                value=str(
                    strategy_config.get(
                        "symbol",
                        "MOCKSTOCK",
                    )
                ),
                placeholder="Example: RELIANCE",
            )

        with basic_right:
            current_timeframe = str(
                strategy_config.get(
                    "timeframe",
                    "1 Minute",
                )
            )

            try:
                timeframe_index = (
                    TIMEFRAME_OPTIONS.index(
                        current_timeframe
                    )
                )
            except ValueError:
                timeframe_index = 0

            timeframe = st.selectbox(
                "Timeframe",
                options=TIMEFRAME_OPTIONS,
                index=timeframe_index,
            )

            enabled = st.toggle(
                "Strategy Enabled",
                value=bool(
                    strategy_config.get(
                        "enabled",
                        True,
                    )
                ),
            )

        st.markdown("---")
        st.markdown("### Entry and Exit Rules")

        rule_left, rule_right = st.columns(2)

        with rule_left:
            buy_threshold = st.number_input(
                "Buy when price is greater than or equal to",
                min_value=0.01,
                value=float(
                    strategy_config.get(
                        "buy_threshold",
                        105.0,
                    )
                ),
                step=0.50,
                format="%.2f",
            )

        with rule_right:
            sell_threshold = st.number_input(
                "Sell when price is less than or equal to",
                min_value=0.01,
                value=float(
                    strategy_config.get(
                        "sell_threshold",
                        95.0,
                    )
                ),
                step=0.50,
                format="%.2f",
            )

        st.info(
            "Current rule: BUY above the buy threshold, "
            "SELL below the sell threshold, otherwise HOLD."
        )

        st.markdown("---")
        st.markdown("### Risk Management")

        risk_col_1, risk_col_2 = st.columns(2)
        risk_col_3, risk_col_4 = st.columns(2)

        with risk_col_1:
            stop_loss_percent = st.number_input(
                "Stop Loss (%)",
                min_value=0.01,
                max_value=100.0,
                value=float(
                    strategy_config.get(
                        "stop_loss_percent",
                        2.0,
                    )
                ),
                step=0.10,
                format="%.2f",
            )

        with risk_col_2:
            target_percent = st.number_input(
                "Target (%)",
                min_value=0.01,
                max_value=100.0,
                value=float(
                    strategy_config.get(
                        "target_percent",
                        4.0,
                    )
                ),
                step=0.10,
                format="%.2f",
            )

        with risk_col_3:
            risk_per_trade_percent = st.number_input(
                "Risk Per Trade (%)",
                min_value=0.01,
                max_value=100.0,
                value=float(
                    strategy_config.get(
                        "risk_per_trade_percent",
                        1.0,
                    )
                ),
                step=0.10,
                format="%.2f",
            )

        with risk_col_4:
            max_position_size_percent = st.number_input(
                "Maximum Position Size (%)",
                min_value=0.01,
                max_value=100.0,
                value=float(
                    strategy_config.get(
                        "max_position_size_percent",
                        10.0,
                    )
                ),
                step=0.50,
                format="%.2f",
            )

        save_button = st.form_submit_button(
            "💾 Save Strategy",
            use_container_width=True,
            type="primary",
        )

    if save_button:
        new_strategy_config = {
            "strategy_name": strategy_name,
            "symbol": symbol,
            "timeframe": timeframe,
            "buy_threshold": float(
                buy_threshold
            ),
            "sell_threshold": float(
                sell_threshold
            ),
            "stop_loss_percent": float(
                stop_loss_percent
            ),
            "target_percent": float(
                target_percent
            ),
            "risk_per_trade_percent": float(
                risk_per_trade_percent
            ),
            "max_position_size_percent": float(
                max_position_size_percent
            ),
            "enabled": bool(enabled),
        }

        success, message = save_strategy_config(
            new_strategy_config
        )

        if success:
            st.success(message)
            st.rerun()

        st.error(message)


def show_strategy_controls(
    strategy_config: dict[str, Any],
) -> None:
    """
    Display separate start and stop controls.
    """

    st.markdown("### Strategy Controls")

    start_column, stop_column = st.columns(2)

    with start_column:
        start_clicked = st.button(
            "▶ Start Strategy",
            use_container_width=True,
            disabled=bool(
                strategy_config.get(
                    "enabled",
                    False,
                )
            ),
        )

    with stop_column:
        stop_clicked = st.button(
            "■ Stop Strategy",
            use_container_width=True,
            disabled=not bool(
                strategy_config.get(
                    "enabled",
                    False,
                )
            ),
        )

    if start_clicked:
        change_strategy_status(
            strategy_config,
            enabled=True,
        )

    if stop_clicked:
        change_strategy_status(
            strategy_config,
            enabled=False,
        )


def show_strategy_page() -> None:
    """
    Render the complete dashboard-based strategy builder.
    """

    strategy_config, load_message = (
        load_strategy_config()
    )

    if "could not" in load_message.lower():
        st.warning(load_message)

    show_strategy_status(strategy_config)
    show_strategy_form(strategy_config)
    show_strategy_controls(strategy_config)