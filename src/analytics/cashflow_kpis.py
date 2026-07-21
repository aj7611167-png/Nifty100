import sqlite3
import pandas as pd

# =====================================================
# PATHS
# =====================================================

DB_PATH = "db/nifty100.db"

OUTPUT_FILE = "output/cashflow_intelligence.xlsx"
DISTRESS_FILE = "output/distress_alerts.csv"

# =====================================================
# CASH FLOW KPI FUNCTIONS
# =====================================================

def free_cash_flow(operating_activity, investing_activity):
    """
    Free Cash Flow = CFO + Investing Cash Flow
    (Investing cash flow is usually negative.)
    """

    if pd.isna(operating_activity) or pd.isna(investing_activity):
        return None

    return round(operating_activity + investing_activity, 2)


def cfo_quality_score(cfo_list, pat_list):
    """
    Average CFO / PAT across years.
    """

    ratios = []

    for cfo, pat in zip(cfo_list, pat_list):

        if pd.isna(cfo) or pd.isna(pat):
            continue

        if pat == 0:
            continue

        ratios.append(cfo / pat)

    if len(ratios) == 0:
        return None

    avg = sum(ratios) / len(ratios)

    if avg >= 1:
        return "High Quality"

    elif avg >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(investing_activity, sales):
    """
    CAPEX Intensity = |Investing Cash Flow| / Sales
    """

    if pd.isna(investing_activity):
        return None, None

    if pd.isna(sales):
        return None, None

    if sales == 0:
        return None, None

    value = abs(investing_activity) / sales * 100
    value = round(value, 2)

    if value < 3:
        label = "Asset Light"

    elif value <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return value, label


def fcf_conversion_rate(fcf, operating_profit):
    """
    FCF as % of Operating Profit.
    """

    if pd.isna(fcf):
        return None

    if pd.isna(operating_profit):
        return None

    if operating_profit == 0:
        return None

    return round((fcf / operating_profit) * 100, 2)



def capital_allocation_pattern(cfo, cfi, cff):
    """
    Classify cash allocation pattern.
    """

    if pd.isna(cfo) or pd.isna(cfi) or pd.isna(cff):
        return "Unknown"

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    mapping = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "+", "-"): "Liquidating Assets",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "-"): "Pre-Revenue",
        ("+", "-", "+"): "Mixed"
    }

    return mapping.get(signs, "Unknown")

def distress_alert(
    operating_activity,
    free_cash_flow,
    cfo_quality,
    debt_to_equity,
    interest_coverage
):
    """
    Classify financial health using cash flow and leverage metrics.
    """

    score = 0

    # Negative operating cash flow
    if pd.notna(operating_activity) and operating_activity < 0:
        score += 1

    # Negative free cash flow
    if pd.notna(free_cash_flow) and free_cash_flow < 0:
        score += 1

    # Poor earnings quality
    if cfo_quality == "Accrual Risk":
        score += 1

    # Highly leveraged company
    if pd.notna(debt_to_equity) and debt_to_equity > 2:
        score += 1

    # Weak ability to pay interest
    if (
        pd.notna(interest_coverage)
        and interest_coverage < 1.5
    ):
        score += 1

    # Final classification
    if score >= 4:
        return "Distress"

    elif score >= 2:
        return "Watchlist"

    return "Healthy"

# =====================================================
# DATABASE FUNCTIONS
# =====================================================

def get_connection():
    """
    Create and return a SQLite database connection.
    """
    return sqlite3.connect(DB_PATH)


def load_data():
    """
    Load all tables required for Cash Flow Intelligence.
    """

    conn = get_connection()

    cashflow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    profit_loss = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    balance_sheet = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    financial_ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    sectors = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )

    conn.close()

    return (
        cashflow,
        profit_loss,
        balance_sheet,
        financial_ratios,
        companies,
        sectors
    )

# =====================================================
# YEAR NORMALIZATION
# =====================================================

def normalize_year(series):
    """
    Convert different year formats to YYYY.

    Examples:
    Mar-13   -> 2013
    Mar 2013 -> 2013
    Mar-2013 -> 2013
    """

    year = (
        series.astype(str)
        .str.extract(r"(\d{2,4})", expand=False)
    )

    year = year.apply(
        lambda x: (
            "20" + x
            if pd.notna(x) and len(str(x)) == 2
            else x
        )
    )

    return year

# =====================================================
# PREPARE MASTER DATA
# =====================================================

def prepare_master_dataframe():
    """
    Merge all required tables into one master dataframe.
    """

    (
        cashflow,
        profit_loss,
        balance_sheet,
        financial_ratios,
        companies,
        sectors
    ) = load_data()

# =====================================================
# NORMALIZE YEAR FORMAT
# =====================================================

    cashflow["year"] = normalize_year(cashflow["year"])
    profit_loss["year"] = normalize_year(profit_loss["year"])
    balance_sheet["year"] = normalize_year(balance_sheet["year"])
    financial_ratios["year"] = normalize_year(financial_ratios["year"])

# =====================================================
# FIX INCONSISTENT COMPANY IDS
# =====================================================

    ticker_mapping = {
        "AGTL": "ATGL",
        "BAJAJ-AUTO": "BAJAJ_AUTO"
    }

    cashflow["company_id"] = cashflow["company_id"].replace(ticker_mapping)
    profit_loss["company_id"] = profit_loss["company_id"].replace(ticker_mapping)
    balance_sheet["company_id"] = balance_sheet["company_id"].replace(ticker_mapping)
    financial_ratios["company_id"] = financial_ratios["company_id"].replace(ticker_mapping)
    companies["id"] = companies["id"].replace(ticker_mapping)
    sectors["company_id"] = sectors["company_id"].replace(ticker_mapping)

# =====================================================
# REMOVE DUPLICATES
# =====================================================
# Some source tables contain duplicate company-year records
# (e.g. TCS, ABB, BAJAJ-AUTO). Deduplicate before merging
# to prevent row multiplication.

    cashflow = (
        cashflow.drop_duplicates(
            subset=["company_id", "year"],
            keep="first"
    )
        .copy()
    )

    profit_loss = (
        profit_loss
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="first"
        )
        .copy()
    )

    balance_sheet = (
        balance_sheet
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="first"
        )
        .copy()
    )

    financial_ratios = (
        financial_ratios
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="first"
        )
        .copy()
    )

    companies = (
        companies
        .drop_duplicates(
            subset=["id"],
            keep="first"
        )
        .copy()
    )

    sectors = (
        sectors
        .drop_duplicates(
            subset=["company_id"],
            keep="first"
        )
        .copy()
    )

# =====================================================
# DROP UNUSED PRIMARY KEYS
# =====================================================

    profit_loss.drop(columns=["id"], errors="ignore", inplace=True)
    balance_sheet.drop(columns=["id"], errors="ignore", inplace=True)
    financial_ratios.drop(columns=["id"], errors="ignore", inplace=True)
    sectors.drop(columns=["id"], errors="ignore", inplace=True)

    companies.rename(
        columns={"id": "company_id"},
        inplace=True
    )
# =====================================================
# MERGES
# =====================================================

    df = cashflow.merge(
        profit_loss,
        on=["company_id", "year"],
        how="left"
    )

    df = df.merge(
        balance_sheet,
        on=["company_id", "year"],
        how="left"
    )

    df = df.merge(
        financial_ratios,
        on=["company_id", "year"],
        how="left"
    )
   
    df = df.merge(
        companies,
        on="company_id",
        how="left"
    )
   
    df = df.merge(
        sectors,
        on="company_id",
        how="left"
    )
   
    return df
# =====================================================
# MAIN
# =====================================================

def main():

    print("=" * 60)
    print("Cash Flow Intelligence")
    print("=" * 60)

    # =====================================================
    # LOAD MASTER DATA
    # =====================================================

    df = prepare_master_dataframe()

    # =====================================================
    # FREE CASH FLOW
    # =====================================================

    df["free_cash_flow"] = df.apply(
        lambda row: free_cash_flow(
            row["operating_activity"],
            row["investing_activity"]
        ),
        axis=1
    )

    # =====================================================
    # FCF CONVERSION RATE
    # =====================================================

    df["fcf_conversion_rate"] = df.apply(
        lambda row: fcf_conversion_rate(
            row["free_cash_flow"],
            row["operating_profit"]
        ),
        axis=1
    )

    # =====================================================
    # CAPEX INTENSITY
    # =====================================================

    df[["capex_intensity", "capex_category"]] = pd.DataFrame(
        df.apply(
            lambda row: capex_intensity(
                row["investing_activity"],
                row["sales"]
            ),
            axis=1
        ).tolist(),
        index=df.index
    )
    # =====================================================
    # CAPITAL ALLOCATION PATTERN
    # =====================================================

    df["capital_allocation"] = df.apply(
        lambda row: capital_allocation_pattern(
            row["operating_activity"],
            row["investing_activity"],
            row["financing_activity"]
        ),
        axis=1
    )

    # =====================================================
    # CFO QUALITY SCORE
    # =====================================================

    quality_scores = {}

    for company, group in df.groupby("company_id"):

        group = group.sort_values("year")

        quality_scores[company] = cfo_quality_score(
            group["operating_activity"].tolist(),
            group["net_profit"].tolist()
        )

    df["cfo_quality"] = df["company_id"].map(quality_scores)

    # =====================================================
    # FINANCIAL DISTRESS ALERT
    # =====================================================

    df["distress_alert"] = df.apply(
        lambda row: distress_alert(
            row["operating_activity"],
            row["free_cash_flow"],
            row["cfo_quality"],
            row["debt_to_equity"],
            row["interest_coverage"]
        ),
        axis=1
    )

    # =====================================================
    # KPI PREVIEW
    # =====================================================

    print("\nCash Flow KPI Preview")
    print("-" * 140)

    print(
        df[
            [
                "company_id",
                "year",
                "free_cash_flow",
                "fcf_conversion_rate",
                "capex_intensity",
                "capex_category",
                "capital_allocation",
                "cfo_quality",
                "distress_alert",
            ]
        ]
        .head(20)
        .to_string(index=False)
    )

    # =====================================================
    # SUMMARY REPORTS
    # =====================================================

    print("\nDistress Summary")
    print("-" * 40)
    print(df["distress_alert"].value_counts(dropna=False))

    print("\nCapital Allocation Summary")
    print("-" * 40)
    print(df["capital_allocation"].value_counts(dropna=False))

    print("\nCFO Quality Summary")
    print("-" * 40)
    print(df["cfo_quality"].value_counts(dropna=False))

    print("\nCAPEX Category Summary")
    print("-" * 40)
    print(df["capex_category"].value_counts(dropna=False))

    # -------------------------------------------------
    # Dataset Information
    # -------------------------------------------------

    print(f"\nRows loaded    : {len(df)}")
    print(f"Columns loaded : {len(df.columns)}")

    print("\nFirst 10 columns:")
    print(df.columns[:10].tolist())

    print("\nData Preview:")
    print(
        df[
            [
                "company_id",
                "year",
                "free_cash_flow",
                "fcf_conversion_rate",
                "capex_intensity",
                "capex_category",
                "capital_allocation",
                "cfo_quality",
                "distress_alert",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    # -------------------------------------------------
    # Export Complete KPI Dataset
    # -------------------------------------------------

    df.to_excel(
        OUTPUT_FILE,
        index=False
    )

    print("\nExcel report saved successfully.")
    print(f"Excel report saved to: {OUTPUT_FILE}")

    # -------------------------------------------------
    # Export Distress Alerts
    # -------------------------------------------------

    distress_df = df[
        df["distress_alert"] != "Healthy"
    ].copy()

    distress_df.to_csv(
        DISTRESS_FILE,
        index=False
    )

    print("\nDistress report saved successfully.")
    print(f"Distress report saved to: {DISTRESS_FILE}")

    print("\n" + "=" * 60)
    print("Cash Flow Intelligence Report Generated Successfully")
    print("=" * 60)

if __name__ == "__main__":
    main()