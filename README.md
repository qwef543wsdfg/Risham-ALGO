# Risham Algo 

A beginner-friendly mock algo trading signal dashboard built with Python and Streamlit.

This project generates simulated stock prices, applies simple trading rules, creates BUY, SELL, or HOLD signals, saves signal history to a CSV file, and displays the latest information on a Streamlit dashboard.

## Important Disclaimer

This project:

- Does not use real market data
- Does not place real orders
- Does not connect to any broker API
- Does not use real money
- Is built only for learning and testing

## Features

- Generates mock stock prices
- Simulates realistic percentage-based price movement
- Applies predefined BUY, SELL, and HOLD rules
- Displays current price
- Displays current signal
- Displays last update time
- Saves signal history to CSV
- Displays recent history on the dashboard
- Automatically refreshes the live section
- Prevents repeated consecutive signal records
- Handles invalid prices and file errors safely
- Validates project configuration

## Trading Rules

The default strategy uses these rules:

- Price above the buy threshold returns `BUY`
- Price below the sell threshold returns `SELL`
- Otherwise, it returns `HOLD`

Default values:

```text
Starting price: 100.0
Buy threshold: 105.0
Sell threshold: 95.0
Update interval: 2 seconds
