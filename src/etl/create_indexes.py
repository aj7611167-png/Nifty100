import sqlite3

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

indexes = [

    ("profitandloss", "company_id"),
    ("profitandloss", "year"),

    ("balancesheet", "company_id"),
    ("balancesheet", "year"),

    ("cashflow", "company_id"),
    ("cashflow", "year"),

    ("financial_ratios", "company_id"),
    ("financial_ratios", "year"),

    ("market_cap", "company_id"),
    ("market_cap", "year"),

    ("stock_prices", "company_id"),
    ("stock_prices", "date"),

    ("documents", "company_id"),
    ("documents", "Year"),

    ("analysis", "company_id"),

    ("peer_groups", "company_id"),

    ("peer_percentiles", "company_id"),
    ("peer_percentiles", "year"),
]

for table, column in indexes:

    cursor.execute(f"""
        CREATE INDEX IF NOT EXISTS
        idx_{table}_{column}
        ON {table}({column});
    """)

conn.commit()
conn.close()

print("All indexes created successfully.")