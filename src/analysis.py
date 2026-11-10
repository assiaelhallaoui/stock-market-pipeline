
import sqlite3
from src.database import DB_PATH


def get_stock_summary():
    """Calculate stock statistics using SQL."""

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            SELECT
                ticker,
                COUNT(*) AS trading_days,
                ROUND(AVG(close), 2) AS avg_price,
                ROUND(MIN(close), 2) AS min_price,
                ROUND(MAX(close), 2) AS max_price,
                ROUND(AVG(volume), 0) AS avg_volume
            FROM stock_prices
            GROUP BY ticker
            ORDER BY ticker
        """)

        return cursor.fetchall()


def get_daily_returns(ticker):
    """Calculate daily percentage returns using SQL."""

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            SELECT
                date,
                ROUND(close, 2) AS closing_price,
                ROUND(
                    100.0 * (close - LAG(close) OVER (
                        PARTITION BY ticker ORDER BY date
                    )) /
                    NULLIF(LAG(close) OVER (
                        PARTITION BY ticker ORDER BY date
                    ), 0),
                    2
                ) AS daily_return_pct
            FROM stock_prices
            WHERE ticker = ?
            ORDER BY date
        """, (ticker,))

        return cursor.fetchall()


if __name__ == "__main__":
    print("\nSTOCK MARKET SUMMARY\n")

    for row in get_stock_summary():
        print(row)

    print("\nAAPL DAILY RETURNS\n")

    for row in get_daily_returns("AAPL")[:10]:
        print(row)

# COUNT(*) nb jours de cotation
# AVG(close) prix moyen de fermeture 
# MIN(close) / max(close)
# AVG(volume) volume moyen exchanged 
# GROUP BY ticker regroupe par company