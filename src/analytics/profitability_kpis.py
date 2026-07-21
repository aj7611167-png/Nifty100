import numpy as np
import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

OUTPUT_FILE = "output/profitability_intelligence.xlsx"
OUTPUT_SUMMARY = "output/profitability_summary.csv"

def get_connection():
    return sqlite3.connect(DB_PATH)

def load_data():
    """
    Load all tables required for Profitability Intelligence.
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
# PREPARE MASTER DATAFRAME
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
    # MERGE ALL TABLES
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
# OPERATING MARGIN ANALYSIS
# =====================================================

def operating_margin_analysis(
    operating_profit,
    sales
):
    """
    Calculate Operating Margin (%) and classify profitability.
    """

    if (
        pd.isna(operating_profit)
        or pd.isna(sales)
        or sales == 0
    ):
        return None, "Unknown"

    margin = round(
        (operating_profit / sales) * 100,
        2
    )

    if margin >= 25:
        category = "Excellent"

    elif margin >= 15:
        category = "Healthy"

    elif margin >= 8:
        category = "Average"

    elif margin >= 0:
        category = "Weak"

    else:
        category = "Loss Making"

    return margin, category

# =====================================================
# NET PROFIT MARGIN ANALYSIS
# =====================================================

def net_profit_margin_analysis(
    net_profit,
    sales
):
    """
    Calculate Net Profit Margin (%) and classify profitability.
    """

    if (
        pd.isna(net_profit)
        or pd.isna(sales)
        or sales == 0
    ):
        return None, "Unknown"

    margin = round(
        (net_profit / sales) * 100,
        2
    )

    if margin >= 20:
        category = "Excellent"

    elif margin >= 10:
        category = "Healthy"

    elif margin >= 5:
        category = "Average"

    elif margin >= 0:
        category = "Weak"

    else:
        category = "Loss Making"

    return margin, category

# =====================================================
# RETURN ON EQUITY (ROE) QUALITY
# =====================================================

def roe_quality(roe):
    """
    Classify Return on Equity (ROE).
    """

    if pd.isna(roe):
        return "Unknown"

    if roe >= 20:
        return "Excellent"

    elif roe >= 15:
        return "Healthy"

    elif roe >= 10:
        return "Average"

    elif roe >= 0:
        return "Weak"

    else:
        return "Negative ROE"

# =====================================================
# RETURN ON ASSETS (ROA) QUALITY
# =====================================================

def roa_quality(
    net_profit,
    total_assets
):
    """
    Calculate Return on Assets (ROA)
    and classify asset efficiency.
    """

    if (
        pd.isna(net_profit)
        or pd.isna(total_assets)
        or total_assets == 0
    ):
        return None, "Unknown"

    roa = round(
        (net_profit / total_assets) * 100,
        2
    )

    if roa >= 10:
        category = "Excellent"

    elif roa >= 5:
        category = "Healthy"

    elif roa >= 2:
        category = "Average"

    elif roa >= 0:
        category = "Weak"

    else:
        category = "Negative"

    return roa, category

# =====================================================
# RETURN ON CAPITAL EMPLOYED (ROCE)
# =====================================================

def roce_quality(roce):
    """
    Classify Return on Capital Employed (ROCE).
    """

    if pd.isna(roce):
        return "Unknown"

    if roce >= 20:
        return "Excellent"

    elif roce >= 15:
        return "Healthy"

    elif roce >= 10:
        return "Average"

    elif roce >= 0:
        return "Weak"

    else:
        return "Negative"
    
# =====================================================
# GROSS PROFIT MARGIN ANALYSIS
# =====================================================

def gross_profit_margin_analysis(
    sales,
    expenses
):
    """
    Calculate Gross Profit Margin (%) and classify profitability.
    """

    if (
        pd.isna(sales)
        or pd.isna(expenses)
        or sales == 0
    ):
        return None, "Unknown"

    gross_profit = sales - expenses

    margin = round(
        (gross_profit / sales) * 100,
        2
    )

    if margin >= 40:
        category = "Excellent"

    elif margin >= 25:
        category = "Healthy"

    elif margin >= 15:
        category = "Average"

    elif margin >= 0:
        category = "Weak"

    else:
        category = "Loss Making"

    return margin, category


# =====================================================
# EBITDA MARGIN ANALYSIS
# =====================================================

def ebitda_margin_analysis(
    operating_profit,
    depreciation,
    sales
):
    """
    Calculate EBITDA Margin (%) and classify profitability.
    """

    if (
        pd.isna(operating_profit)
        or pd.isna(depreciation)
        or pd.isna(sales)
        or sales == 0
    ):
        return None, "Unknown"

    ebitda = operating_profit + depreciation

    margin = round(
        (ebitda / sales) * 100,
        2
    )

    if margin >= 30:
        category = "Excellent"

    elif margin >= 20:
        category = "Healthy"

    elif margin >= 10:
        category = "Average"

    elif margin >= 0:
        category = "Weak"

    else:
        category = "Loss Making"

    return margin, category


# =====================================================
# INTEREST COVERAGE ANALYSIS
# =====================================================

def interest_coverage_quality(coverage):
    """
    Classify Interest Coverage Ratio.
    """

    if pd.isna(coverage):
        return "Unknown"

    if coverage >= 10:
        return "Excellent"

    elif coverage >= 5:
        return "Healthy"

    elif coverage >= 2:
        return "Average"

    elif coverage >= 1:
        return "Weak"

    else:
        return "Danger"


# =====================================================
# PAT GROWTH ANALYSIS
# =====================================================

def pat_growth_analysis(growth):
    """
    Classify PAT Growth.
    """

    if pd.isna(growth):
        return "Unknown"

    if growth >= 20:
        return "Excellent"

    elif growth >= 10:
        return "Healthy"

    elif growth >= 0:
        return "Stable"

    else:
        return "Declining"


# =====================================================
# EPS GROWTH ANALYSIS
# =====================================================

def eps_growth_analysis(growth):
    """
    Classify EPS Growth.
    """

    if pd.isna(growth):
        return "Unknown"

    if growth >= 20:
        return "Excellent"

    elif growth >= 10:
        return "Healthy"

    elif growth >= 0:
        return "Stable"

    else:
        return "Declining"
    
# =====================================================
# COMPOSITE PROFITABILITY SCORE
# =====================================================

def profitability_score(row):
    """
    Overall Profitability Score (0-8)
    """

    score = 0

    if row["operating_margin_category"] == "Excellent":
        score += 1

    if row["net_profit_margin_category"] == "Excellent":
        score += 1

    if row["roe_quality"] == "Excellent":
        score += 1

    if row["roa_quality"] == "Excellent":
        score += 1

    if row["roce_quality"] == "Excellent":
        score += 1

    if row["ebitda_margin_category"] == "Excellent":
        score += 1

    if row["interest_coverage_quality"] == "Excellent":
        score += 1

    if row["pat_growth_quality"] == "Excellent":
        score += 1

    return score

# =====================================================
# EARNINGS QUALITY SCORE
# =====================================================

def earnings_quality_score(row):
    """
    Calculate a composite earnings quality score.
    """

    score = 0

    # Operating Margin
    if pd.notna(row["operating_margin"]):
        score += min(row["operating_margin"], 30)

    # Net Profit Margin
    if pd.notna(row["net_profit_margin"]):
        score += min(row["net_profit_margin"], 25)

    # ROE
    if pd.notna(row["return_on_equity_pct"]):
        score += min(row["return_on_equity_pct"], 20)

    # ROCE
    if pd.notna(row["roce_percentage"]):
        score += min(row["roce_percentage"], 15)

    # Interest Coverage
    if pd.notna(row["interest_coverage"]):
        score += min(row["interest_coverage"] / 2, 10)

    return round(score, 2)

# =====================================================
# PROFITABILITY RANKING
# =====================================================

def profitability_ranking(score):
    """
    Assign profitability rank based on composite profitability score (0-8).
    """

    if pd.isna(score):
        return "Unknown"

    if score >= 8:
        return "Platinum"

    elif score >= 6:
        return "Gold"

    elif score >= 4:
        return "Silver"

    elif score >= 2:
        return "Bronze"

    else:
        return "Poor"
    
# =====================================================
# MAIN
# =====================================================

def main():

    print("=" * 60)
    print("Profitability Intelligence")
    print("=" * 60)

    # =====================================================
    # LOAD MASTER DATA
    # =====================================================

    df = prepare_master_dataframe()

    # =====================================================
    # OPERATING MARGIN ANALYSIS
    # =====================================================

    df[["operating_margin", "operating_margin_category"]] = pd.DataFrame(
        df.apply(
            lambda row: operating_margin_analysis(
                row["operating_profit"],
                row["sales"]
            ),
            axis=1
        ).tolist(),
        index=df.index
    )

    # =====================================================
    # NET PROFIT MARGIN ANALYSIS
    # =====================================================

    df[["net_profit_margin", "net_profit_margin_category"]] = pd.DataFrame(
        df.apply(
            lambda row: net_profit_margin_analysis(
                row["net_profit"],
                row["sales"]
            ),
            axis=1
        ).tolist(),
        index=df.index
    )

    # =====================================================
    # ROE QUALITY
    # =====================================================

    df["roe_quality"] = df["return_on_equity_pct"].apply(
        roe_quality
    )

    # =====================================================
    # ROA
    # =====================================================

    df[["return_on_assets_pct", "roa_quality"]] = pd.DataFrame(
        df.apply(
            lambda row: roa_quality(
                row["net_profit"],
                row["total_assets"]
            ),
            axis=1
        ).tolist(),
        index=df.index
    )

    # =====================================================
    # ROCE QUALITY
    # =====================================================

    df["roce_quality"] = df["roce_percentage"].apply(
        roce_quality
    )

    # =====================================================
    # GROSS PROFIT MARGIN
    # =====================================================

    df[["gross_profit_margin", "gross_profit_margin_category"]] = pd.DataFrame(
        df.apply(
            lambda row: gross_profit_margin_analysis(
                row["sales"],
                row["expenses"]
            ),
            axis=1
        ).tolist(),
        index=df.index
    )

    # =====================================================
    # EBITDA MARGIN
    # =====================================================

    df[["ebitda_margin", "ebitda_margin_category"]] = pd.DataFrame(
        df.apply(
            lambda row: ebitda_margin_analysis(
                row["operating_profit"],
                row["depreciation"],
                row["sales"]
            ),
            axis=1
        ).tolist(),
        index=df.index
    )

    # =====================================================
    # INTEREST COVERAGE QUALITY
    # =====================================================

    df["interest_coverage_quality"] = df["interest_coverage"].apply(
        interest_coverage_quality
    )

    # =====================================================
    # PAT GROWTH
    # =====================================================

    df = df.sort_values(
        ["company_id", "year"]
    )

    df["pat_growth_pct"] = (
        df.groupby("company_id")["net_profit"]
          .pct_change() * 100
    )

    df["pat_growth_pct"] = df["pat_growth_pct"].round(2)

    # =====================================================
    # EPS GROWTH
    # =====================================================

    eps_column = (
        "earnings_per_share"
        if "earnings_per_share" in df.columns
        else "eps"
    )

    df["eps_growth_pct"] = (
        df.groupby("company_id")[eps_column]
          .pct_change() * 100
    )

    df["eps_growth_pct"] = df["eps_growth_pct"].round(2)

    # =====================================================
    # REMOVE INFINITE VALUES
    # =====================================================

    df["pat_growth_pct"] = df["pat_growth_pct"].replace(
        [np.inf, -np.inf],
        np.nan
    )

    df["eps_growth_pct"].replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    # =====================================================
    # PAT GROWTH QUALITY
    # =====================================================

    df["pat_growth_quality"] = df["pat_growth_pct"].apply(
        pat_growth_analysis
    )

    # =====================================================
    # EPS GROWTH QUALITY
    # =====================================================

    df["eps_growth_quality"] = df["eps_growth_pct"].apply(
        eps_growth_analysis
    )

    # =====================================================
    # COMPOSITE PROFITABILITY SCORE
    # =====================================================

    df["profitability_score"] = df.apply(
        profitability_score,
        axis=1
    )

    # =====================================================
    # EARNINGS QUALITY SCORE
    # =====================================================

    df["earnings_quality_score"] = df.apply(
        earnings_quality_score,
        axis=1
    )

    # =====================================================
    # PROFITABILITY RANKING
    # =====================================================

    df["profitability_rank"] = df["profitability_score"].apply(
        profitability_ranking
    )

    # =====================================================
    # KPI PREVIEW
    # =====================================================

    print("\nProfitability KPI Preview")
    print("-" * 190)

    print(
        df[
            [
                "company_id",
                "year",
                "operating_margin",
                "operating_margin_category",
                "net_profit_margin",
                "net_profit_margin_category",
                "return_on_equity_pct",
                "roe_quality",
                "return_on_assets_pct",
                "roa_quality",
                "roce_percentage",
                "roce_quality",
                "gross_profit_margin",
                "gross_profit_margin_category",
                "ebitda_margin",
                "ebitda_margin_category",
                "interest_coverage",
                "interest_coverage_quality",
                "pat_growth_pct",
                "pat_growth_quality",
                "eps_growth_pct",
                "eps_growth_quality",
                "profitability_score",
                "earnings_quality_score",
                "profitability_rank"
            ]
        ]
        .head(20)
        .to_string(index=False)
    )

    # =====================================================
    # TOP 20 PROFITABLE COMPANIES
    # =====================================================

    print("\nTop 20 Most Profitable Companies")
    print("-" * 120)

    top20 = (
        df.sort_values(
            "profitability_score",
            ascending=False
        )
        [
            [
                "company_id",
                "year",
                "profitability_score",
                "profitability_rank",
                "earnings_quality_score",
                "operating_margin",
                "net_profit_margin",
                "return_on_equity_pct",
                "roce_percentage"
            ]
        ]
        .head(20)
    )

    print(top20.to_string(index=False))

# =====================================================
# BOTTOM 20 COMPANIES
# =====================================================

    print("\nBottom 20 Companies")
    print("-" * 120)

    bottom20 = (
        df.sort_values(
            "profitability_score",
            ascending=True
        )
        [
            [
                "company_id",
                "year",
                "profitability_score",
                "profitability_rank",
                "earnings_quality_score",
                "operating_margin",
                "net_profit_margin",
                "return_on_equity_pct",
                "roce_percentage"
            ]
        ]
        .head(20)
    )

    print(bottom20.to_string(index=False))

    # =====================================================
    # SUMMARY REPORTS
    # =====================================================

    print("\nOperating Margin Summary")
    print("-" * 40)
    print(df["operating_margin_category"].value_counts(dropna=False))

    print("\nNet Profit Margin Summary")
    print("-" * 40)
    print(df["net_profit_margin_category"].value_counts(dropna=False))

    print("\nROE Quality Summary")
    print("-" * 40)
    print(df["roe_quality"].value_counts(dropna=False))

    print("\nROA Quality Summary")
    print("-" * 40)
    print(df["roa_quality"].value_counts(dropna=False))

    print("\nROCE Quality Summary")
    print("-" * 40)
    print(df["roce_quality"].value_counts(dropna=False))

    print("\nGross Profit Margin Summary")
    print("-" * 40)
    print(df["gross_profit_margin_category"].value_counts(dropna=False))

    print("\nEBITDA Margin Summary")
    print("-" * 40)
    print(df["ebitda_margin_category"].value_counts(dropna=False))

    print("\nInterest Coverage Summary")
    print("-" * 40)
    print(df["interest_coverage_quality"].value_counts(dropna=False))

    print("\nPAT Growth Summary")
    print("-" * 40)
    print(df["pat_growth_quality"].value_counts(dropna=False))

    print("\nEPS Growth Summary")
    print("-" * 40)
    print(df["eps_growth_quality"].value_counts(dropna=False))

    print("\nProfitability Score Summary")
    print("-" * 40)
    print(df["profitability_score"].value_counts().sort_index())

    print("\nProfitability Ranking Summary")
    print("-" * 40)
    print(df["profitability_rank"].value_counts())

    # =====================================================
    # DATASET INFORMATION
    # =====================================================

    print("\nRows loaded    :", len(df))
    print("Columns loaded :", len(df.columns))

    print("\nFirst 10 columns:")
    print(df.columns[:10].tolist())

    print("\nData Preview:")

    print(
        df[
            [
                "company_id",
                "year",
                "operating_margin",
                "net_profit_margin",
                "return_on_equity_pct",
                "return_on_assets_pct",
                "roce_percentage",
                "gross_profit_margin",
                "ebitda_margin",
                "interest_coverage",
                "pat_growth_pct",
                "eps_growth_pct",
                "profitability_score",
                "earnings_quality_score",
                "profitability_rank",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    # =====================================================
    # EXPORT REPORTS
    # =====================================================

    df.to_excel(
        OUTPUT_FILE,
        index=False
    )

    print("\nExcel report saved successfully.")
    print(f"Profitability report saved to: {OUTPUT_FILE}")

    summary = pd.DataFrame({
        "Operating Margin": df["operating_margin_category"].value_counts(),
        "Net Profit Margin": df["net_profit_margin_category"].value_counts(),
        "ROE Quality": df["roe_quality"].value_counts(),
        "ROA Quality": df["roa_quality"].value_counts(),
        "ROCE Quality": df["roce_quality"].value_counts(),
        "Gross Profit Margin": df["gross_profit_margin_category"].value_counts(),
        "EBITDA Margin": df["ebitda_margin_category"].value_counts(),
        "Interest Coverage": df["interest_coverage_quality"].value_counts(),
        "PAT Growth": df["pat_growth_quality"].value_counts(),
        "EPS Growth": df["eps_growth_quality"].value_counts(),
        "Profitability Ranking": df["profitability_rank"].value_counts(),
    }).fillna(0)

    summary.to_csv(
        OUTPUT_SUMMARY,
        index=True
    )

    print("Summary report saved successfully.")
    print(f"Summary report saved to: {OUTPUT_SUMMARY}")

    print("\n" + "=" * 60)
    print("Profitability Intelligence Report Generated Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()