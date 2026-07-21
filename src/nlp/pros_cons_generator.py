import sqlite3
import pandas as pd

# =====================================================
# PATHS
# =====================================================

DB_PATH = "db/nifty100.db"

OUTPUT_FILE = "output/pros_cons_generated.csv"

# =====================================================
# DATABASE FUNCTIONS
# =====================================================

def get_connection():
    """
    Create and return a SQLite connection.
    """
    return sqlite3.connect(DB_PATH)


def load_financial_data():
    """
    Load the latest financial ratios together with company names.
    """

    conn = get_connection()

    query = """
    SELECT
        fr.*,
        c.company_name
    FROM financial_ratios fr
    LEFT JOIN companies c
        ON fr.company_id = c.id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

# =====================================================
# PREPARE DATA
# =====================================================

def prepare_data(df):
    """
    Clean financial data and keep only the latest
    available record for each company.
    """

    # Convert important columns to numeric

    numeric_columns = [
        "return_on_equity_pct",
        "operating_profit_margin_pct",
        "debt_to_equity",
        "interest_coverage",
        "free_cash_flow_cr",
        "earnings_per_share",
        "dividend_payout_ratio_pct",
        "total_debt_cr",
        "cash_from_operations_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "composite_quality_score",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # Sort by company and year

    df = df.sort_values(
        ["company_id", "year"]
    )

    # Keep only latest record

    latest_df = (
        df.groupby("company_id")
          .tail(1)
          .reset_index(drop=True)
    )

    return latest_df

# =====================================================
# GENERATE PROS & CONS
# =====================================================

def generate_pros_cons(df):
    """
    Generate rule-based Pros and Cons for each company.
    """

    records = []

    for _, row in df.iterrows():

        company_id = row["company_id"]

        roe = row["return_on_equity_pct"]
        debt = row["debt_to_equity"]
        fcf = row["free_cash_flow_cr"]
        opm = row["operating_profit_margin_pct"]
        revenue_cagr = row["revenue_cagr_5yr"]
        pat_cagr = row["pat_cagr_5yr"]
        eps_cagr = row["eps_cagr_5yr"]
        icr = row["interest_coverage"]
        payout = row["dividend_payout_ratio_pct"]
        quality = row["composite_quality_score"]

        # -------------------------------------------------
        # PRO RULES
        # -------------------------------------------------

        # =====================================================
        # PRO RULE 1
        # ROE > 20%
        # =====================================================

        if pd.notna(roe) and roe > 20:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Pro",
                    "rule_id": "P1",
                    "text": "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",
                    "confidence_pct": 90,
                }
            )

        # =====================================================
        # PRO RULE 2
        # Positive Free Cash Flow
        # =====================================================

        if pd.notna(fcf) and fcf > 0:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Pro",
                    "rule_id": "P2",
                    "text": "Strong free cash flow generation indicates healthy business fundamentals.",
                    "confidence_pct": 85,
                }
            )

        # =====================================================
        # PRO RULE 3
        # Debt Free
        # =====================================================

        if pd.notna(debt) and debt == 0:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Pro",
                    "rule_id": "P3",
                    "text": "Debt-free balance sheet provides financial flexibility and eliminates interest burden.",
                    "confidence_pct": 90,
                }
            )
        
        # =====================================================
        # PRO RULE 4
        # Revenue CAGR > 15%
        # =====================================================

        if pd.notna(revenue_cagr) and revenue_cagr > 15:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Pro",
                    "rule_id": "P4",
                    "text": "Revenue growing above 15% CAGR reflects strong business momentum.",
                    "confidence_pct": 85,
                }
            )

        # =====================================================
        # PRO RULE 5
        # Operating Margin > 25%
        # =====================================================

        if pd.notna(opm) and opm > 25:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Pro",
                    "rule_id": "P5",
                    "text": "Operating profit margin above 25% indicates strong pricing power and cost discipline.",
                    "confidence_pct": 80,
                }
            )

        # =====================================================
        # PRO RULE 6
        # PAT CAGR > 20%
        # =====================================================

        if pd.notna(pat_cagr) and pat_cagr > 20:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Pro",
                    "rule_id": "P6",
                    "text": "Net profit compounding above 20% over five years creates significant shareholder value.",
                    "confidence_pct": 90,
                }
            )

        # =====================================================
        # PRO RULE 7
        # Interest Coverage > 10 OR Debt Free
        # =====================================================

        if (pd.notna(icr) and icr > 10) or (pd.notna(debt) and debt == 0):

            records.append(
                {
                    "company_id": company_id,
                    "type": "Pro",
                    "rule_id": "P7",
                    "text": "Very high interest coverage reflects negligible financial stress from debt servicing.",
                    "confidence_pct": 85,
                }
            )

        # =====================================================
        # PRO RULE 8
        # Dividend payout with positive FCF
        # =====================================================

        if (
            pd.notna(payout)
            and payout > 2
            and pd.notna(fcf)
            and fcf > 0
        ):

            records.append(
                {
                    "company_id": company_id,
                    "type": "Pro",
                    "rule_id": "P8",
                    "text": "Consistent dividend payout backed by positive free cash flow reflects healthy shareholder returns.",
                    "confidence_pct": 80,
                }
            )

        # =====================================================
        # PRO RULE 9
        # EPS CAGR > 15%
        # =====================================================

        if pd.notna(eps_cagr) and eps_cagr > 15:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Pro",
                    "rule_id": "P9",
                    "text": "Earnings per share growing above 15% CAGR indicates strong earnings quality.",
                    "confidence_pct": 85,
                }
            )

        # =====================================================
        # PRO RULE 10
        # Composite Quality Score
        # =====================================================

        if pd.notna(quality) and quality >= 20:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Pro",
                    "rule_id": "P10",
                    "text": "High composite quality score reflects consistently strong financial performance.",
                    "confidence_pct": 80,
                }
            )

        # =====================================================
        # PRO RULE 11
        # Revenue CAGR greater than PAT CAGR
        # =====================================================

        if (
            pd.notna(revenue_cagr)
            and pd.notna(pat_cagr)
            and revenue_cagr > pat_cagr
        ):

            records.append(
                {
                    "company_id": company_id,
                    "type": "Pro",
                    "rule_id": "P11",
                    "text": "Revenue growth exceeding profit growth indicates stable operating expansion.",
                    "confidence_pct": 75,
                }
            )

        # =====================================================
        # PRO RULE 12
        # Strong Balance Sheet
        # =====================================================

        if (
            pd.notna(debt)
            and debt < 0.5
            and pd.notna(quality)
            and quality >= 20
        ):

            records.append(
                {
                    "company_id": company_id,
                    "type": "Pro",
                    "rule_id": "P12",
                    "text": "Strong balance sheet with low leverage supports sustainable long-term growth.",
                    "confidence_pct": 90,
                }
            )

        # -------------------------------------------------
        # CON RULES
        # -------------------------------------------------

        # =====================================================
        # CON RULE 1
        # Debt to Equity > 2
        # =====================================================

        if pd.notna(debt) and debt > 2:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Con",
                    "rule_id": "C1",
                    "text": f"Debt-to-equity ratio of {debt:.2f} is elevated and warrants monitoring.",
                    "confidence_pct": 90,
                }
            )

        # =====================================================
        # CON RULE 2
        # Negative Free Cash Flow
        # =====================================================

        if pd.notna(fcf) and fcf < 0:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Con",
                    "rule_id": "C2",
                    "text": "Negative free cash flow raises concern about cash generation quality.",
                    "confidence_pct": 85,
                }
            )

        # =====================================================
        # CON RULE 3
        # Operating Margin below 10%
        # =====================================================

        if pd.notna(opm) and opm < 10:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Con",
                    "rule_id": "C3",
                    "text": "Operating margin below 10% indicates weak operating profitability.",
                    "confidence_pct": 80,
                }
            )

        # =====================================================
        # CON RULE 4
        # ROE below 10%
        # =====================================================

        if pd.notna(roe) and roe < 10:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Con",
                    "rule_id": "C4",
                    "text": "Return on equity below 10% suggests inefficient capital utilization.",
                    "confidence_pct": 80,
                }
            )

                # =====================================================
        # CON RULE 5
        # Revenue CAGR below 5%
        # =====================================================

        if pd.notna(revenue_cagr) and revenue_cagr < 5:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Con",
                    "rule_id": "C5",
                    "text": "Revenue growth below 5% indicates weak business momentum.",
                    "confidence_pct": 80,
                }
            )

        # =====================================================
        # CON RULE 6
        # Interest Coverage below 1.5
        # =====================================================

        if pd.notna(icr) and icr < 1.5:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Con",
                    "rule_id": "C6",
                    "text": "Interest coverage below 1.5x indicates elevated debt servicing risk.",
                    "confidence_pct": 90,
                }
            )

        # =====================================================
        # CON RULE 7
        # Dividend Payout above 100%
        # =====================================================

        if pd.notna(payout) and payout > 100:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Con",
                    "rule_id": "C7",
                    "text": "Dividend payout above 100% may not be sustainable over the long term.",
                    "confidence_pct": 85,
                }
            )

        # =====================================================
        # CON RULE 8
        # Low Composite Quality Score
        # =====================================================

        if pd.notna(quality) and quality < 10:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Con",
                    "rule_id": "C8",
                    "text": "Low composite quality score reflects weak overall financial quality.",
                    "confidence_pct": 85,
                }
            )

                # =====================================================
        # CON RULE 9
        # EPS CAGR below 5%
        # =====================================================

        if pd.notna(eps_cagr) and eps_cagr < 5:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Con",
                    "rule_id": "C9",
                    "text": "Earnings per share growth below 5% indicates weak earnings momentum.",
                    "confidence_pct": 80,
                }
            )

        # =====================================================
        # CON RULE 10
        # ROE below 15%
        # =====================================================

        if pd.notna(roe) and roe < 15:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Con",
                    "rule_id": "C10",
                    "text": "Return on equity below 15% suggests the business is generating modest shareholder returns.",
                    "confidence_pct": 75,
                }
            )

        # =====================================================
        # CON RULE 11
        # High Debt with Low Interest Coverage
        # =====================================================

        if (
            pd.notna(debt)
            and pd.notna(icr)
            and debt > 1.5
            and icr < 3
        ):

            records.append(
                {
                    "company_id": company_id,
                    "type": "Con",
                    "rule_id": "C11",
                    "text": "High leverage combined with weak interest coverage increases financial risk.",
                    "confidence_pct": 90,
                }
            )

        # =====================================================
        # CON RULE 12
        # Negative Composite Quality Score Signal
        # =====================================================

        if (
            pd.notna(quality)
            and quality < 15
            and pd.notna(revenue_cagr)
            and revenue_cagr < 10
        ):

            records.append(
                {
                    "company_id": company_id,
                    "type": "Con",
                    "rule_id": "C12",
                    "text": "Weak quality score together with slow revenue growth indicates limited business strength.",
                    "confidence_pct": 85,
                }
            )

                # =====================================================
        # FALLBACK PRO
        # =====================================================

        company_records = [
            r for r in records
            if r["company_id"] == company_id and r["type"] == "Pro"
        ]

        if len(company_records) == 0:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Pro",
                    "rule_id": "PF",
                    "text": "The company maintains an established business presence within its industry.",
                    "confidence_pct": 65,
                }
            )

                # =====================================================
        # FALLBACK CON
        # =====================================================

        company_records = [
            r for r in records
            if r["company_id"] == company_id and r["type"] == "Con"
        ]

        if len(company_records) == 0:

            records.append(
                {
                    "company_id": company_id,
                    "type": "Con",
                    "rule_id": "CF",
                    "text": "The company should continue improving financial performance across key metrics.",
                    "confidence_pct": 65,
                }
            )

    return pd.DataFrame(records)

# =====================================================
# MAIN
# =====================================================

def main():

    print("=" * 60)
    print("Pros & Cons Generator")
    print("=" * 60)

    # Load data
    df = load_financial_data()

    print(f"Financial rows loaded : {len(df)}")

    # Keep latest year only
    latest_df = prepare_data(df)

    print(f"Latest company rows   : {len(latest_df)}")

    # Generate Pros & Cons
    output_df = generate_pros_cons(latest_df)

    # Keep only confidence > 60
    output_df = output_df[
        output_df["confidence_pct"] > 60
    ]

    # Save CSV
    output_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Records generated     : {len(output_df)}")

    print("\nOutput File:")
    print(f"✓ {OUTPUT_FILE}")

    print("=" * 60)

if __name__ == "__main__":
    main()