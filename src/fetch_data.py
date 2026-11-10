
import yfinance as yf
from src.database import create_database, save_stock_data, get_stock_data


def fetch_stock_data(ticker, period="1mo"):
    """Retrieve historical stock prices."""

    stock = yf.Ticker(ticker)
    data = stock.history(period=period)

    if data.empty:
        print(f"No data found for {ticker}")
        return None

    return data


if __name__ == "__main__":

    create_database()

    tickers = ["AAPL", "MSFT", "NVDA"]

    for ticker in tickers:
        print(f"\nFetching {ticker}...")

        data = fetch_stock_data(ticker)

        if data is not None:
            save_stock_data(ticker, data)

            stored_data = get_stock_data(ticker)

            print("First 5 rows from SQLite:")
            for row in stored_data[:5]:
                print(row)


# data categories
# open, high, low, close, volume 
