
import sqlite3

from src import database


def test_database_creation(tmp_path, monkeypatch):
    test_db = tmp_path / "test_stocks.db"
    monkeypatch.setattr(database, "DB_PATH", test_db)

    database.create_database()

    assert test_db.exists()

    with sqlite3.connect(test_db) as conn:
        table = conn.execute("""
            SELECT name FROM sqlite_master
            WHERE type = 'table' AND name = 'stock_prices'
        """).fetchone()

    assert table is not None


def test_no_duplicate_prices(tmp_path, monkeypatch):
    import pandas as pd

    test_db = tmp_path / "test_stocks.db"
    monkeypatch.setattr(database, "DB_PATH", test_db)

    database.create_database()

    data = pd.DataFrame(
        {
            "Open": [100.0],
            "High": [105.0],
            "Low": [98.0],
            "Close": [103.0],
            "Volume": [1000000],
        },
        index=pd.to_datetime(["2026-11-09"])
    )

    database.save_stock_data("AAPL", data)
    database.save_stock_data("AAPL", data)

    with sqlite3.connect(test_db) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM stock_prices"
        ).fetchone()[0]

    assert count == 1
