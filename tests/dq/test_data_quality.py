import sqlite3
from pathlib import Path

DB_PATH = Path("db/nifty100.db")

EXPECTED_TABLES = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "sectors",
    "stock_prices",
    "financial_ratios",
    "peer_groups",
    "market_cap",
]


def test_database_exists():
    assert DB_PATH.exists()


def test_database_connection():
    conn = sqlite3.connect(DB_PATH)
    assert conn is not None
    conn.close()


def test_all_tables_exist():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )

    tables = {row[0] for row in cursor.fetchall()}

    conn.close()

    for table in EXPECTED_TABLES:
        assert table in tables


def test_companies_has_rows():
    conn = sqlite3.connect(DB_PATH)

    count = conn.execute(
        "SELECT COUNT(*) FROM companies"
    ).fetchone()[0]

    conn.close()

    assert count > 0


def test_financial_ratios_has_rows():
    conn = sqlite3.connect(DB_PATH)

    count = conn.execute(
        "SELECT COUNT(*) FROM financial_ratios"
    ).fetchone()[0]

    conn.close()

    assert count > 0


def test_market_cap_has_rows():
    conn = sqlite3.connect(DB_PATH)

    count = conn.execute(
        "SELECT COUNT(*) FROM market_cap"
    ).fetchone()[0]

    conn.close()

    assert count > 0