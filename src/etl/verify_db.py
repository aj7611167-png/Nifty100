import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

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

for t in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {t}")
    print(t, cursor.fetchone()[0])

conn.close()