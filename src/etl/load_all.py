import pandas as pd
import sqlite3
from pathlib import Path

DB_PATH = "db/nifty100.db"

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

FILES = {
    "companies.xlsx": "companies",
    "profitandloss.xlsx": "profitandloss",
    "balancesheet.xlsx": "balancesheet",
    "cashflow.xlsx": "cashflow",
    "analysis.xlsx": "analysis",
    "documents.xlsx": "documents",
    "prosandcons.xlsx": "prosandcons",
    "sectors.xlsx": "sectors",
    "stock_prices.xlsx": "stock_prices",
    "financial_ratios.xlsx": "financial_ratios",
    "peer_groups.xlsx": "peer_groups",
    "market_cap.xlsx": "market_cap"
}

MESSY_HEADERS = {
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx"
}

conn = sqlite3.connect(DB_PATH)

for file_name, table_name in FILES.items():

    path = RAW_DIR / file_name

    if not path.exists():
        print(f"Missing file: {path}")
        continue

    try:
        if file_name in MESSY_HEADERS:
            df = pd.read_excel(path, header=1)
        else:
            df = pd.read_excel(path)

        # Basic sanity check
        if df.empty:
            print(f"Empty file: {file_name}")
            continue

        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        print(f"Loaded {table_name} -> {len(df)} rows")

    except Exception as e:
        print(f"Error loading {file_name}: {e}")

conn.close()

print("DONE: All tables loaded")