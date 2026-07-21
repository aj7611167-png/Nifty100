import re
import sqlite3
import pandas as pd

# =====================================================
# PATHS
# =====================================================

DB_PATH = "db/nifty100.db"

OUTPUT_PARSED = "output/analysis_parsed.csv"

OUTPUT_FAILURES = "output/parse_failures.csv"

# =====================================================
# REGEX PATTERN
# =====================================================

PATTERN = re.compile(
    r"(\d+)\s*Years?:?\s*([\d.]+)%"
)

# =====================================================
# DATABASE FUNCTIONS
# =====================================================

def get_connection():
    """
    Create and return a SQLite database connection.
    """
    return sqlite3.connect(DB_PATH)


def load_analysis():
    """
    Load the analysis table from SQLite.
    """
    conn = get_connection()

    query = """
    SELECT
        company_id,
        compounded_sales_growth,
        compounded_profit_growth,
        stock_price_cagr,
        roe
    FROM analysis
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# =====================================================
# PARSE METRIC
# =====================================================

def parse_metric(text):
    """
    Parse text such as:

        10 Years: 21%
        5 Years       17%
        3 Years:9%

    Ignore:

        TTM
        Last Year

    Returns

        (period_years, value_pct)

    or

        ("IGNORE", "IGNORE")

    or

        (None, None)
    """

    if pd.isna(text):
        return None, None

    text = str(text).strip()

    if text == "":
        return None, None

    # Ignore metrics that Sprint 5 doesn't require

    if text.startswith("TTM"):
        return "IGNORE", "IGNORE"

    if text.startswith("Last Year"):
        return "IGNORE", "IGNORE"

    match = PATTERN.search(text)

    if match:

        period_years = int(match.group(1))
        value_pct = float(match.group(2))

        return period_years, value_pct

    return None, None


# =====================================================
# PROCESS ANALYSIS DATA
# =====================================================

def process_analysis(df):
    """
    Parse all analysis fields.

    Returns

    parsed_df
    failures_df
    """

    parsed_records = []

    failed_records = []

    ignored_records = 0

    metrics = {
        "compounded_sales_growth": "Sales CAGR",
        "compounded_profit_growth": "Profit CAGR",
        "stock_price_cagr": "Stock CAGR",
        "roe": "ROE"
    }

    for _, row in df.iterrows():

        company_id = row["company_id"]

        for column_name, metric_name in metrics.items():

            text = row[column_name]

            period, value = parse_metric(text)

            # Ignore TTM / Last Year

            if period == "IGNORE":

                ignored_records += 1

                continue

            # Parsed successfully

            if period is not None:

                parsed_records.append(
                    {
                        "company_id": company_id,
                        "metric_type": metric_name,
                        "period_years": period,
                        "value_pct": value
                    }
                )

            # Failed parsing

            else:

                failed_records.append(
                    {
                        "company_id": company_id,
                        "metric_type": metric_name,
                        "original_text": text
                    }
                )

    parsed_df = pd.DataFrame(parsed_records)

    failures_df = pd.DataFrame(failed_records)

    return parsed_df, failures_df, ignored_records


# =====================================================
# MAIN
# =====================================================

def main():

    print("=" * 60)
    print("NLP Analysis Parser")
    print("=" * 60)

    analysis_df = load_analysis()

    print(f"Analysis rows loaded : {len(analysis_df)}")

    parsed_df, failures_df, ignored = process_analysis(
        analysis_df
    )

    parsed_df.to_csv(
        OUTPUT_PARSED,
        index=False
    )

    failures_df.to_csv(
        OUTPUT_FAILURES,
        index=False
    )

    print(f"Parsed records       : {len(parsed_df)}")
    print(f"Ignored records      : {ignored}")
    print(f"Failed records       : {len(failures_df)}")

    print("\nFiles generated successfully:")

    print(f"✓ {OUTPUT_PARSED}")

    print(f"✓ {OUTPUT_FAILURES}")

    print("=" * 60)


if __name__ == "__main__":
    main()