"""
Professional Plotly chart components for Algo Trading V2.
"""

from html import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


CHART_LINE_COLOR = "#5b7cff"
CHART_POSITIVE_COLOR = "#22c97a"
CHART_NEGATIVE_COLOR = "#ff5c75"
CHART_NEUTRAL_COLOR = "#94a3b8"

CHART_BACKGROUND = "rgba(0, 0, 0, 0)"
CHART_GRID_COLOR = "rgba(148, 163, 184, 0.09)"
CHART_AXIS_COLOR = "#64748b"
CHART_TEXT_COLOR = "#94a3b8"


def _prepare_price_data(
    price_history: list[float],
) -> list[float]:
    """
    Return valid positive numeric prices.
    """

    valid_prices: list[float] = []

    for price in price_history:
        try:
            numeric_price = float(price)

            if numeric_price > 0:
                valid_prices.append(numeric_price)

        except (TypeError, ValueError):
            continue

    return valid_prices


def _get_price_direction(
    current_price: float,
    previous_price: float,
) -> str:
    """
    Return positive, negative or neutral direction.
    """

    if current_price > previous_price:
        return "positive"

    if current_price < previous_price:
        return "negative"

    return "neutral"


def _get_direction_color(
    direction: str,
) -> str:
    """
    Return the color associated with price direction.
    """

    if direction == "positive":
        return CHART_POSITIVE_COLOR

    if direction == "negative":
        return CHART_NEGATIVE_COLOR

    return CHART_NEUTRAL_COLOR


def _calculate_price_change(
    current_price: float,
    previous_price: float,
) -> tuple[float, float]:
    """
    Calculate absolute and percentage price movement.
    """

    absolute_change = current_price - previous_price

    if previous_price <= 0:
        return absolute_change, 0.0

    percentage_change = (
        absolute_change / previous_price
    ) * 100

    return absolute_change, percentage_change


def _get_change_symbol(
    price_change: float,
) -> str:
    """
    Return the appropriate price movement symbol.
    """

    if price_change > 0:
        return "▲"

    if price_change < 0:
        return "▼"

    return "•"


def _get_change_prefix(
    price_change: float,
) -> str:
    """
    Return plus sign for positive values.
    """

    return "+" if price_change > 0 else ""


def _render_chart_header(
    current_price: float,
    previous_price: float,
    minimum_price: float,
    maximum_price: float,
) -> None:
    """
    Render the chart header and market statistics.
    """

    direction = _get_price_direction(
        current_price=current_price,
        previous_price=previous_price,
    )

    absolute_change, percentage_change = (
        _calculate_price_change(
            current_price=current_price,
            previous_price=previous_price,
        )
    )

    change_symbol = _get_change_symbol(
        absolute_change
    )

    change_prefix = _get_change_prefix(
        absolute_change
    )

    chart_header = (
        '<div class="plotly-chart-header">'
        '<div class="plotly-chart-heading">'
        '<div class="panel-eyebrow">MARKET DATA</div>'
        '<div class="panel-title">Live Price Chart</div>'
        '</div>'

        '<div class="plotly-chart-stats">'

        '<div class="plotly-chart-stat">'
        '<span>Low</span>'
        f'<strong>₹{minimum_price:,.2f}</strong>'
        '</div>'

        '<div class="plotly-chart-stat">'
        '<span>High</span>'
        f'<strong>₹{maximum_price:,.2f}</strong>'
        '</div>'

        f'<div class="plotly-current-price price-{direction}">'
        '<span>Current Price</span>'
        f'<strong>₹{current_price:,.2f}</strong>'
        f'<small>{change_symbol} '
        f'{change_prefix}{absolute_change:,.2f} '
        f'({change_prefix}{percentage_change:.2f}%)'
        '</small>'
        '</div>'

        '</div>'
        '</div>'
    )

    st.markdown(
        chart_header,
        unsafe_allow_html=True,
    )


def _build_price_dataframe(
    prices: list[float],
) -> pd.DataFrame:
    """
    Build chart data with update numbers.
    """

    return pd.DataFrame(
        {
            "Update": range(
                1,
                len(prices) + 1,
            ),
            "Price": prices,
        }
    )


def _calculate_y_axis_range(
    prices: list[float],
) -> list[float]:
    """
    Return a tightly padded Y-axis domain.

    This prevents the graph from appearing compressed
    or stuck at the top of the chart.
    """

    minimum_price = min(prices)
    maximum_price = max(prices)

    price_range = maximum_price - minimum_price

    if price_range == 0:
        padding = max(
            minimum_price * 0.01,
            1.0,
        )
    else:
        padding = max(
            price_range * 0.12,
            minimum_price * 0.002,
            0.25,
        )

    lower_bound = max(
        minimum_price - padding,
        0.01,
    )

    upper_bound = maximum_price + padding

    return [
        lower_bound,
        upper_bound,
    ]


def _build_gradient_fill_color() -> str:
    """
    Return transparent line-area fill color.

    Plotly does not use CSS gradients inside a standard
    scatter trace, so a restrained translucent fill is used.
    """

    return "rgba(91, 124, 255, 0.13)"


def _build_price_figure(
    chart_data: pd.DataFrame,
    current_price: float,
    direction: str,
) -> go.Figure:
    """
    Build the interactive institutional price chart.
    """

    direction_color = _get_direction_color(direction)

    prices = chart_data["Price"].tolist()
    updates = chart_data["Update"].tolist()

    y_axis_range = _calculate_y_axis_range(prices)

    first_price = prices[0]

    change_from_start = [
        (
            ((price - first_price) / first_price) * 100
            if first_price > 0
            else 0.0
        )
        for price in prices
    ]

    hover_data = list(
        zip(
            updates,
            change_from_start,
        )
    )

    figure = go.Figure()

    # Soft glow under the primary line
    figure.add_trace(
        go.Scatter(
            x=updates,
            y=prices,
            mode="lines",
            name="Price Glow",
            line={
                "color": "rgba(91, 124, 255, 0.20)",
                "width": 10,
                "shape": "spline",
                "smoothing": 0.75,
            },
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # Main institutional price line
    figure.add_trace(
        go.Scatter(
            x=updates,
            y=prices,
            mode="lines",
            name="Market Price",
            line={
                "color": CHART_LINE_COLOR,
                "width": 3.5,
                "shape": "spline",
                "smoothing": 0.75,
            },
            fill="tozeroy",
            fillgradient={
                "type": "vertical",
                "colorscale": [
                    [0.0, "rgba(91, 124, 255, 0.00)"],
                    [0.55, "rgba(91, 124, 255, 0.08)"],
                    [1.0, "rgba(91, 124, 255, 0.30)"],
                ],
            },
            customdata=hover_data,
            hovertemplate=(
                "<b>Market Update %{customdata[0]}</b><br>"
                "Price: ₹%{y:,.2f}<br>"
                "Session Change: %{customdata[1]:+.2f}%"
                "<extra></extra>"
            ),
            showlegend=False,
        )
    )

    # Outer glow for latest price
    figure.add_trace(
        go.Scatter(
            x=[updates[-1]],
            y=[current_price],
            mode="markers",
            marker={
                "size": 24,
                "color": direction_color,
                "opacity": 0.15,
                "line": {
                    "width": 0,
                },
            },
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # Latest price marker
    figure.add_trace(
        go.Scatter(
            x=[updates[-1]],
            y=[current_price],
            mode="markers",
            name="Current Price",
            marker={
                "size": 11,
                "color": direction_color,
                "line": {
                    "color": "#e8eef8",
                    "width": 2,
                },
            },
            hovertemplate=(
                "<b>Current Price</b><br>"
                "₹%{y:,.2f}"
                "<extra></extra>"
            ),
            showlegend=False,
        )
    )

    # Current-price horizontal reference line
    figure.add_hline(
        y=current_price,
        line_width=1,
        line_dash="dot",
        line_color=direction_color,
        opacity=0.65,
        annotation_text=f"₹{current_price:,.2f}",
        annotation_position="top right",
        annotation_font={
            "color": direction_color,
            "size": 11,
            "family": "Inter, Arial, sans-serif",
        },
        annotation_bgcolor="rgba(6, 15, 28, 0.96)",
        annotation_bordercolor=direction_color,
        annotation_borderwidth=1,
        annotation_borderpad=5,
    )

    figure.update_layout(
        height=520,

        margin={
            "l": 22,
            "r": 70,
            "t": 26,
            "b": 38,
        },

        paper_bgcolor=CHART_BACKGROUND,
        plot_bgcolor=CHART_BACKGROUND,

        font={
            "family": "Inter, Arial, sans-serif",
            "color": CHART_TEXT_COLOR,
            "size": 12,
        },

        showlegend=False,

        hovermode="x unified",

        hoverlabel={
            "bgcolor": "#0d1829",
            "bordercolor": "#32415c",
            "font": {
                "color": "#f1f5f9",
                "family": "Inter, Arial, sans-serif",
                "size": 12,
            },
            "align": "left",
        },

        dragmode="zoom",

        xaxis={
            "title": None,
            "showgrid": True,
            "gridcolor": "rgba(148, 163, 184, 0.045)",
            "gridwidth": 1,
            "showline": True,
            "linecolor": "rgba(148, 163, 184, 0.14)",
            "tickfont": {
                "color": CHART_AXIS_COLOR,
                "size": 10,
            },
            "ticks": "",
            "zeroline": False,
            "fixedrange": False,
            "showspikes": True,
            "spikecolor": "rgba(148, 163, 184, 0.48)",
            "spikethickness": 1,
            "spikedash": "dot",
            "spikemode": "across",
            "spikesnap": "cursor",
            "automargin": True,
        },

        yaxis={
            "title": None,
            "range": y_axis_range,
            "showgrid": True,
            "gridcolor": "rgba(148, 163, 184, 0.075)",
            "gridwidth": 1,
            "showline": False,
            "tickfont": {
                "color": CHART_AXIS_COLOR,
                "size": 10,
            },
            "ticks": "",
            "tickprefix": "₹",
            "tickformat": ",.2f",
            "zeroline": False,
            "fixedrange": False,
            "side": "right",
            "automargin": True,
            "showspikes": True,
            "spikecolor": "rgba(148, 163, 184, 0.48)",
            "spikethickness": 1,
            "spikedash": "dot",
            "spikemode": "across",
            "spikesnap": "cursor",
        },

        modebar={
            "orientation": "v",
            "bgcolor": "rgba(8, 17, 30, 0.92)",
            "color": "#718096",
            "activecolor": "#8ea2ff",
        },

        hoverdistance=100,
        spikedistance=-1,

        uirevision="risham-live-price-chart",
    )

    return figure
def _render_chart_footer(
    update_count: int,
) -> None:
    """
    Render market feed information.
    """

    safe_caption = escape(
        f"{update_count} market updates"
    )

    footer_html = (
        '<div class="plotly-chart-footer">'
        f'<span>{safe_caption}</span>'
        '<span class="plotly-live-indicator">'
        '<span class="plotly-live-dot"></span>'
        'Live mock market feed'
        '</span>'
        '</div>'
    )

    st.markdown(
        footer_html,
        unsafe_allow_html=True,
    )


def _render_empty_chart() -> None:
    """
    Render an empty chart state.
    """

    st.markdown(
        (
            '<div class="plotly-chart-empty">'
            '<div class="plotly-chart-empty-icon">⌁</div>'
            '<div class="plotly-chart-empty-title">'
            'Waiting for market data'
            '</div>'
            '<div class="plotly-chart-empty-text">'
            'The chart will appear after valid market prices '
            'are collected.'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def show_price_chart(
    price_history: list[float],
) -> None:
    """
    Render the live Plotly market-price chart.

    Args:
        price_history:
            Ordered sequence of recent market prices.
    """

    valid_prices = _prepare_price_data(
        price_history
    )

    if not valid_prices:
        _render_empty_chart()
        return

    current_price = valid_prices[-1]

    previous_price = (
        valid_prices[-2]
        if len(valid_prices) >= 2
        else current_price
    )

    minimum_price = min(valid_prices)
    maximum_price = max(valid_prices)

    direction = _get_price_direction(
        current_price=current_price,
        previous_price=previous_price,
    )

    _render_chart_header(
        current_price=current_price,
        previous_price=previous_price,
        minimum_price=minimum_price,
        maximum_price=maximum_price,
    )

    chart_data = _build_price_dataframe(
        valid_prices
    )

    figure = _build_price_figure(
        chart_data=chart_data,
        current_price=current_price,
        direction=direction,
    )

    st.plotly_chart(
        figure,
        width="stretch",
        config={
            "displaylogo": False,
            "scrollZoom": True,
            "responsive": True,
            "modeBarButtonsToRemove": [
                "lasso2d",
                "select2d",
                "autoScale2d",
            ],
            "toImageButtonOptions": {
                "format": "png",
                "filename": "risham_live_price_chart",
                "height": 720,
                "width": 1280,
                "scale": 2,
            },
        },
        key="live_price_plotly_chart",
    )

    _render_chart_footer(
        update_count=len(valid_prices)
    )