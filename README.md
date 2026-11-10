# Stock Market Data Pipeline

A Python-based financial data pipeline that retrieves historical stock market data, stores it in a SQLite database, performs SQL-based analysis, and visualizes market trends through an interactive Streamlit dashboard.

## Features

- Retrieve historical stock prices for Apple (AAPL), Microsoft (MSFT), and NVIDIA (NVDA) using yfinance.
- Store OHLCV market data in SQLite with duplicate prevention.
- Analyze average, minimum, and maximum closing prices and trading volumes using SQL.
- Calculate daily percentage returns using SQL window functions.
- Visualize historical prices, trading volumes, and daily returns.
- Compare the percentage performance of multiple stocks.
- Display 7-day and 20-day simple moving averages.
- Refresh market data directly from the dashboard.
- Run automated database tests with pytest.

## Tech Stack

- **Python** — Data processing and application logic
- **SQLite / SQL** — Persistent storage and financial queries
- **Pandas** — Data manipulation and moving averages
- **yfinance** — Historical market data retrieval
- **Streamlit** — Interactive web dashboard
- **Plotly** — Financial data visualization
- **pytest** — Automated testing

## Project Structure

```text
stock-market-pipeline/
├── app.py
├── src/
│   ├── fetch_data.py
│   ├── database.py
│   └── analysis.py
├── data/
├── tests/
│   └── test_database.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository and navigate to the project directory.

```bash
git clone https://github.com/assiaelhallaoui/stock-market-pipeline.git
cd stock-market-pipeline
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Fetch and store historical market data:

```bash
python -m src.fetch_data
```

Run SQL-based financial analysis:

```bash
python -m src.analysis
```

Launch the dashboard:

```bash
python -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Testing

Run automated tests:

```bash
python -m pytest -v
```

The tests verify database creation and duplicate prevention.

## Data Source

Historical market data is retrieved using yfinance, which accesses Yahoo Finance data. This project is intended for educational and personal use.

## Future Improvements

- Support additional stock tickers.
- Add customizable historical date ranges.
- Implement scheduled data updates.
- Add advanced financial indicators.
- Deploy the dashboard online.
