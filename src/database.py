
import sqlite3
from pathlib import Path

# database location
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "stocks.db"


def create_database():
    # create the stock prices table if it does not exist.

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn: # create SQL table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stock_prices (
                ticker TEXT NOT NULL,
                date TEXT NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                PRIMARY KEY (ticker, date)
            )
        """)


def save_stock_data(ticker, data):
    """Save historical stock data to SQLite."""

    rows = []

    for date, row in data.iterrows():
        rows.append((
            ticker,
            date.strftime("%Y-%m-%d"),
            float(row["Open"]),
            float(row["High"]),
            float(row["Low"]),
            float(row["Close"]),
            int(row["Volume"])
        ))

    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany("""
            INSERT OR REPLACE INTO stock_prices
            (ticker, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, rows)

    print(f"Saved {len(rows)} rows for {ticker}")


def get_stock_data(ticker):
    """Retrieve stored stock prices from SQLite."""

    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("""
            SELECT date, close, volume
            FROM stock_prices
            WHERE ticker = ?
            ORDER BY date
        """, (ticker,)).fetchall()
