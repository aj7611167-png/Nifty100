import pandas as pd
from pathlib import Path

# ==========================================================
# CONFIGURATION
# ==========================================================

RAW_DATA_DIR = Path("data/raw")

FILES = {
    "companies.xlsx": 1,
    "profitandloss.xlsx": 1,
    "balancesheet.xlsx": 1,
    "cashflow.xlsx": 1,
    "analysis.xlsx": 1,
    "documents.xlsx": 1,
    "prosandcons.xlsx": 1,
    "sectors.xlsx": 0,
    "stock_prices.xlsx": 0,
    "financial_ratios.xlsx": 0,
    "peer_groups.xlsx": 0,
    "market_cap.xlsx": 0,
}


# ==========================================================
# FUNCTIONS
# ==========================================================

def inspect_excel(file_name, header_row):
    """
    Read an Excel file and display its structure.
    """

    path = RAW_DATA_DIR / file_name

    print("=" * 80)
    print(f"FILE : {file_name}")
    print("=" * 80)

    if not path.exists():
        print("❌ File not found")
        print(path)
        print()
        return

    try:
        df = pd.read_excel(path, header=header_row)

        print(f"Rows    : {len(df)}")
        print(f"Columns : {len(df.columns)}")
        print(f"Shape   : {df.shape}")

        print("\nColumn Names:")
        for i, column in enumerate(df.columns, start=1):
            print(f"{i:2}. {column}")

        print("\nFirst 5 Rows:")
        print(df.head())

        print()

    except Exception as e:
        print(f"❌ Error reading file: {e}")
        print()


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("\nInspecting Excel files...\n")

    for file_name, header_row in FILES.items():
        inspect_excel(file_name, header_row)

    print("=" * 80)
    print("Inspection Complete")
    print("=" * 80)


if __name__ == "__main__":
    main()