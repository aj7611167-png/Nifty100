import pandas as pd
import sqlite3

DB_PATH = "db/nifty100.db"

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

conn = sqlite3.connect(DB_PATH)

for file_name, table_name in FILES.items():

    path = f"data/raw/{file_name}"

    # ONLY these files have messy headers
    if file_name in [
        "companies.xlsx",
        "profitandloss.xlsx",
        "balancesheet.xlsx",
        "cashflow.xlsx",
        "analysis.xlsx",
        "documents.xlsx",
        "prosandcons.xlsx"
    ]:
        df = pd.read_excel(path, header=1)
    else:
        df = pd.read_excel(path)

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {table_name} -> {len(df)} rows")

conn.close()

print("DONE: All tables loaded")