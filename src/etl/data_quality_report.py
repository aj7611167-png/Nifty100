import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
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
    "market_cap"
]

for table in tables:

    df = pd.read_sql(
        f"SELECT * FROM {table}",
        conn
    )

    print("\n" + "=" * 50)
    print(table)

    print("Rows:", len(df))

    print("Duplicate Rows:", df.duplicated().sum())

    print("Null Values:")
    print(df.isnull().sum())

conn.close()