"""
Chart components for the Algo Trading V2 dashboard.
"""

import pandas as pd
import streamlit as st


def show_price_chart(price_history: list[float]) -> None:
    """
    Display recent mock-market prices as a line chart.

    Args:
        price_history: Ordered list of recent market prices.
    """

    st.markdown(
        """
<div class="panel-card">
    <div class="panel-title">Price Trend</div>
</div>
""",
        unsafe_allow_html=True,
    )

    if not price_history:
        st.info("Price chart will appear after market data is collected.")
        return

    valid_prices: list[float] = []

    for price in price_history:
        try:
            numeric_price = float(price)

            if numeric_price > 0:
                valid_prices.append(numeric_price)

        except (TypeError, ValueError):
            continue

    if not valid_prices:
        st.warning("No valid price history is available.")
        return

    chart_data = pd.DataFrame(
        {
            "Price": valid_prices,
        }
    )

    chart_data.index.name = "Update"

    minimum_price = min(valid_prices)
    maximum_price = max(valid_prices)

    price_padding = max(
        (maximum_price - minimum_price) * 0.20,
        1.0,
    )

    st.line_chart(
        chart_data,
        y="Price",
        height=360,
        use_container_width=True,
    )

    st.caption(
        f"Showing {len(valid_prices)} recent prices · "
        f"Range: ₹{minimum_price:.2f} – ₹{maximum_price:.2f}"
    )