import yfinance as yf
import pandas as pd
import time
from app import app

if __name__ == "__main__":
    app.run(debug=True)


def get_stock_data(symbol):
    try:
        # Fetch real-time data for the given stock symbol from NSE
        stock_data = yf.Ticker(symbol + ".NS")

        # Get current stock information
        stock_info = stock_data.info

        # Extract relevant information
        company_name = stock_info.get("longName", "N/A")
        current_price = stock_info.get("lastClose", "N/A")
        day_high = stock_info.get("dayHigh", "N/A")
        day_low = stock_info.get("dayLow", "N/A")

        # Print the real-time stock information
        print(f"Real-time Data for {symbol}:")
        print(f"Company Name: {company_name}")
        print(f"Current Price: {current_price} INR")
        print(f"Day High: {day_high} INR")
        print(f"Day Low: {day_low} INR")

        return stock_data

    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def get_historical_data(symbol, start_date, end_date):
    try:
        # Fetch historical data for the given stock symbol from NSE
        stock_data = yf.download(symbol + ".NS", start=start_date, end=end_date)

        # Print the historical stock data
        print(f"Historical Data for {symbol} from {start_date} to {end_date}:")
        print(stock_data)

    except Exception as e:
        print(f"Error occurred: {e}")


def stream_real_time_data(symbol):
    try:
        # Set up the yfinance streamer for real-time data
        stock_data = yf.Ticker(symbol + ".NS")
        while True:
            # Get real-time data
            data = stock_data.history(period="1d")
            print(f"Real-time Data for {symbol} (Streaming):")
            print(data.tail(1))  # Print the most recent data
            time.sleep(5)  # Wait for 5 seconds before fetching the next data

    except Exception as e:
        print(f"Error occurred: {e}")


# Example usage
if __name__ == "__main__":
    stock_symbol = input("Enter the stock symbol (e.g., TCS, RELIANCE): ")
    get_stock_data(stock_symbol)  # Fetch real-time data
    start_date = input("Enter start date for historical data (YYYY-MM-DD): ")
    end_date = input("Enter end date for historical data (YYYY-MM-DD): ")
    get_historical_data(stock_symbol, start_date, end_date)  # Fetch historical data
    stream_real_time = input("Do you want to stream real-time data? (yes/no): ")
    if stream_real_time.lower() == "yes":
        stream_real_time_data(stock_symbol)  # Stream real-time data
