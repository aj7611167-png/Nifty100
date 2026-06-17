import pandas as pd
from pathlib import Path

RAW_DATA_DIR = Path("data/raw")

special_files = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
]

normal_files = [
    "sectors.xlsx",
    "stock_prices.xlsx",
    "financial_ratios.xlsx",
    "peer_groups.xlsx",
    "market_cap.xlsx",
]

for file in special_files:
    path = RAW_DATA_DIR / file

    df = pd.read_excel(path, header=1)

    print(f"\n{file}")
    print(df.columns.tolist())
    print(df.shape)

for file in normal_files:
    path = RAW_DATA_DIR / file

    df = pd.read_excel(path)

    print(f"\n{file}")
    print(df.columns.tolist())
    print(df.shape)