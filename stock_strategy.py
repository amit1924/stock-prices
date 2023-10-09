import yfinance as yf
import pandas as pd


def get_stock_data(symbol, start, end):
    try:
        stock_data = yf.download(symbol, start=start, end=end)
        return stock_data
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def moving_average_strategy(stock_data, short_window=50, long_window=200):
    stock_data["Short_MA"] = (
        stock_data["Close"].rolling(window=short_window, min_periods=1).mean()
    )
    stock_data["Long_MA"] = (
        stock_data["Close"].rolling(window=long_window, min_periods=1).mean()
    )

    signals = pd.DataFrame(index=stock_data.index)
    signals["Buy_Signal"] = 0
    signals["Sell_Signal"] = 0

    signals["Buy_Signal"][short_window:] = (
        stock_data["Short_MA"][short_window:] > stock_data["Long_MA"][short_window:]
    )
    signals["Sell_Signal"][short_window:] = (
        stock_data["Short_MA"][short_window:] < stock_data["Long_MA"][short_window:]
    )

    return signals


if __name__ == "__main__":
    # Replace 'AAPL' with the stock symbol you want to analyze
    stock_symbol = "AAPL"
    start_date = "2020-01-01"
    end_date = "2021-01-01"

    # Get historical stock data
    stock_data = get_stock_data(stock_symbol, start=start_date, end=end_date)

    if stock_data is not None:
        # Apply moving average strategy
        signals = moving_average_strategy(stock_data)

        # Print buy/sell signals
        print(signals)
