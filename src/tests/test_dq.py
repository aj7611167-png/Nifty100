import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

financial_ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

peer_groups = pd.read_sql(
    "SELECT * FROM peer_groups",
    conn
)

peer_percentiles = pd.read_sql(
    "SELECT * FROM peer_percentiles",
    conn
)

conn.close()

print("=" * 50)
print("DATA QUALITY REPORT")
print("=" * 50)

print(f"Companies: {len(companies)}")
print(f"Financial Ratios: {len(financial_ratios)}")
print(f"Peer Groups: {len(peer_groups)}")
print(f"Peer Percentiles: {len(peer_percentiles)}")