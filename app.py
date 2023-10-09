from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import numpy as np

app = Flask(__name__)


def get_stock_data(symbol):
    try:
        # Fetch real-time data for the given stock symbol from NSE
        stock_data = yf.Ticker(symbol + ".NS")

        # Get historical data for the last 7 days (adjust as needed)
        historical_data = stock_data.history(period="7d")

        # Extract relevant information
        company_name = stock_data.info.get("longName", "N/A")
        current_price = stock_data.history(period="1d").iloc[-1]["Close"]
        day_high = historical_data["High"].max()
        day_low = historical_data["Low"].min()

        # Prepare timestamp and close price data for the chart
        timestamps = historical_data.index.strftime("%Y-%m-%dT%H:%M:%S").tolist()
        close_prices = historical_data["Close"].tolist()

        return {
            "company_name": company_name,
            "symbol": symbol,
            "current_price": current_price,
            "day_high": day_high,
            "day_low": day_low,
            "timestamps": timestamps,
            "close_prices": close_prices,
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        # Return default values in case of error
        return {
            "company_name": "N/A",
            "symbol": symbol,
            "current_price": 0,
            "day_high": 0,
            "day_low": 0,
            "timestamps": [],
            "close_prices": [],
        }


def moving_average_strategy(close_prices, short_window=5, long_window=20):
    try:
        short_rolling = close_prices.rolling(window=short_window, min_periods=1).mean()
        long_rolling = close_prices.rolling(window=long_window, min_periods=1).mean()

        signals = pd.DataFrame(index=close_prices.index)
        signals["short_mavg"] = short_rolling
        signals["long_mavg"] = long_rolling
        signals["signal"] = 0.0
        signals["signal"][short_window:] = np.where(
            short_rolling[short_window:] > long_rolling[short_window:], 1.0, 0.0
        )

        return signals
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    stock_data = None
    strategy_result = pd.DataFrame()  # Set a default empty DataFrame

    if request.method == "POST":
        symbol = request.form["symbol"]
        if symbol:
            stock_data = get_stock_data(symbol)
            # Call the strategy function
            if stock_data and "close_prices" in stock_data:
                close_prices = stock_data["close_prices"]
                strategy_result = moving_average_strategy(close_prices)

    return render_template(
        "index.html", stock_data=stock_data, strategy_result=strategy_result
    )


if __name__ == "__main__":
    app.run(debug=True)
