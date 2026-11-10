
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st
from src.fetch_data import fetch_stock_data
from src.database import create_database, save_stock_data, get_stock_data

from src.database import DB_PATH


st.set_page_config(
    page_title="Stock Market Dashboard",
    layout="wide"
)

st.title("Stock Market Dashboard")

if st.button("Refresh Market Data"):

    with st.spinner("Updating stock prices..."):
        create_database()

        updated = []
        failed = []

        for symbol in ["AAPL", "MSFT", "NVDA"]:
            try:
                data = fetch_stock_data(symbol, period="1mo")

                if data is not None and not data.empty:
                    save_stock_data(symbol, data)
                    updated.append(symbol)
                else:
                    failed.append(symbol)

            except Exception as error:
                failed.append(symbol)
                st.error(f"{symbol}: {error}")

    if updated:
        st.success(f"Updated: {', '.join(updated)}")

    if failed:
        st.warning(f"Could not update: {', '.join(failed)}")

st.caption("Historical stock market data analysis")


def load_data(ticker):
    """Load historical prices from SQLite."""
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            """
            SELECT date, open, high, low, close, volume
            FROM stock_prices
            WHERE ticker = ?
            ORDER BY date
            """,
            conn,
            params=(ticker,)
        )

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        df["daily_return"] = df["close"].pct_change() * 100

    return df


with sqlite3.connect(DB_PATH) as conn:
    tickers = pd.read_sql_query(
        "SELECT DISTINCT ticker FROM stock_prices ORDER BY ticker",
        conn
    )["ticker"].tolist()

if not tickers:
    st.warning("No stock data available. Run fetch_data.py first.")
    st.stop()

ticker = st.selectbox("Select a stock", tickers)

df = load_data(ticker)

st.subheader(f"{ticker} — Price Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Latest Close", f"${df['close'].iloc[-1]:.2f}")
col2.metric("Average Close", f"${df['close'].mean():.2f}")
col3.metric("Minimum Close", f"${df['close'].min():.2f}")
col4.metric("Maximum Close", f"${df['close'].max():.2f}")


# Calculate simple moving averages
df["SMA_7"] = df["close"].rolling(window=7).mean()
df["SMA_20"] = df["close"].rolling(window=20).mean()

# Select indicators
show_sma7 = st.checkbox("Show 7-day SMA", value=True)
show_sma20 = st.checkbox("Show 20-day SMA", value=True)

# Build price chart
fig = px.line(
    df,
    x="date",
    y="close",
    title=f"{ticker} Closing Price & Moving Averages",
    labels={"date": "Date", "close": "Price (USD)"}
)

if show_sma7:
    fig.add_scatter(
        x=df["date"],
        y=df["SMA_7"],
        mode="lines",
        name="SMA 7"
    )

if show_sma20:
    fig.add_scatter(
        x=df["date"],
        y=df["SMA_20"],
        mode="lines",
        name="SMA 20"
    )

st.plotly_chart(fig, use_container_width=True)


st.subheader("Daily Returns (%)")

fig_returns = px.bar(
    df,
    x="date",
    y="daily_return",
    labels={"date": "Date", "daily_return": "Return (%)"}
)

st.plotly_chart(fig_returns, use_container_width=True)

st.subheader("Trading Volume")

fig_volume = px.bar(
    df,
    x="date",
    y="volume",
    labels={"date": "Date", "volume": "Volume"}
)

st.plotly_chart(fig_volume, use_container_width=True)

with st.expander("View Raw Data"):
    st.dataframe(df, use_container_width=True)


st.divider()
st.subheader("Stock Performance Comparison")

selected_tickers = st.multiselect(
    "Select stocks to compare",
    tickers,
    default=tickers
)

if selected_tickers:
    comparison = []

    for symbol in selected_tickers:
        stock_df = load_data(symbol)

        if stock_df.empty:
            continue

        stock_df["performance"] = (
            stock_df["close"] / stock_df["close"].iloc[0] - 1
        ) * 100

        stock_df["ticker"] = symbol
        comparison.append(
            stock_df[["date", "ticker", "performance"]]
        )

    if comparison:
        comparison_df = pd.concat(comparison, ignore_index=True)

        fig_comparison = px.line(
            comparison_df,
            x="date",
            y="performance",
            color="ticker",
            title="Stock Performance Comparison (%)",
            labels={
                "date": "Date",
                "performance": "Return (%)",
                "ticker": "Stock"
            }
        )

        st.plotly_chart(fig_comparison, use_container_width=True)
