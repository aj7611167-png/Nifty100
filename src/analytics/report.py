from src.analytics.comparison import (
    rank_peer_group,
    get_benchmark_company
)

import sqlite3

import pandas as pd

from src.screener.engine import (
    load_master_dataframe,
    calculate_composite_score
)

DB_PATH = "db/nifty100.db"


def get_connection():

    return sqlite3.connect(DB_PATH)

def load_company_data():

    df = load_master_dataframe()

    df = calculate_composite_score(df)

    return df

def get_company(df, company_id):

    company = df[
        df["company_id"] == company_id
    ]

    if company.empty:

        return None

    return company.iloc[0]

def generate_company_report(company_id):

    df = load_company_data()

    company = get_company(df, company_id)

    if company is None:

        print("Company not found.")

        return

    print("\n" + "=" * 60)
    print("COMPANY REPORT")
    print("=" * 60)

    print(f"Company              : {company['company_name']}")
    print(f"Ticker               : {company['company_id']}")
    print(f"Sector               : {company['sub_sector']}")
    print(f"Market Cap Category  : {company['market_cap_category']}")
    print(f"Quality Score        : {company['quality_score']:.2f}")

    print("\n" + "-" * 60)
    print("FINANCIAL METRICS")
    print("-" * 60)

    print(f"ROE                  : {company['return_on_equity_pct']:.2f}%")
    print(f"ROCE                 : {company['roce_percentage']:.2f}%")
    print(f"Debt / Equity        : {company['debt_to_equity']:.2f}")
    print(f"Revenue CAGR         : {company['revenue_cagr_5yr']:.2f}%")
    print(f"PAT CAGR             : {company['pat_cagr_5yr']:.2f}%")
    print(f"EPS CAGR             : {company['eps_cagr_5yr']:.2f}%")
    print(f"Free Cash Flow       : ₹{company['free_cash_flow_cr']:,.0f} Cr")
    print(f"P/E Ratio            : {company['pe_ratio']:.2f}")
    print(f"P/B Ratio            : {company['pb_ratio']:.2f}")
    print(f"Dividend Yield       : {company['dividend_yield_pct']:.2f}%")

    print("\n" + "-" * 60)
    print("PEER ANALYSIS")
    print("-" * 60)

    ranking = rank_peer_group(company_id)

    benchmark = get_benchmark_company(company_id)

    company_rank = ranking.loc[
        ranking["company_id"] == company_id,
        "rank"
    ].iloc[0]

    total_companies = len(ranking)

    overall_score = ranking.loc[
        ranking["company_id"] == company_id,
        "overall_percentile"
    ].iloc[0]

    print(f"Peer Group           : {company['sub_sector']}")
    print(f"Rank                 : {company_rank} / {total_companies}")
    print(f"Overall Percentile   : {overall_score:.2f}")
    print(f"Benchmark Company    : {benchmark}")


if __name__ == "__main__":

    generate_company_report("TCS")
