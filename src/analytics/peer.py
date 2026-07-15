import sqlite3
import pandas as pd

from src.screener.engine import load_master_dataframe


# ==========================================================
# LOAD DATA
# ==========================================================

def load_peer_groups():

    return pd.read_excel(
        "docs/data/raw/peer_groups.xlsx"
    )


def prepare_peer_dataframe():

    financial = load_master_dataframe()

    peers = load_peer_groups()

    df = financial.merge(
        peers,
        on="company_id",
        how="left"
    )

    return df


# ==========================================================
# SQLITE
# ==========================================================

def create_peer_percentiles_table():

    conn = sqlite3.connect("db/nifty100.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS peer_percentiles (

        company_id TEXT,

        peer_group_name TEXT,

        metric TEXT,

        value REAL,

        percentile_rank REAL,

        year INTEGER

    )
    """)

    conn.commit()

    conn.close()

    print("peer_percentiles table created successfully.")


# ==========================================================
# PERCENTILE FUNCTION
# ==========================================================

def calculate_percentile(series, inverse=False):

    if inverse:
        return (1 - series.rank(pct=True)) * 100

    return series.rank(pct=True) * 100


# ==========================================================
# METRICS
# ==========================================================

metrics = [
    "return_on_equity_pct",
    "roce_percentage",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "eps_cagr_5yr",
    "interest_coverage",
    "asset_turnover"
]


# ==========================================================
# MAIN
# ==========================================================

def save_peer_percentiles(percentile_df):

    conn = sqlite3.connect("db/nifty100.db")

    cursor = conn.cursor()

    # Remove old records
    cursor.execute("DELETE FROM peer_percentiles")

    for _, row in percentile_df.iterrows():

        for metric in metrics:

            cursor.execute(
                """
                INSERT INTO peer_percentiles
                (
                    company_id,
                    peer_group_name,
                    metric,
                    value,
                    percentile_rank,
                    year
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    row["company_id"],
                    row["peer_group_name"],
                    metric,
                    row[metric],
                    row[f"{metric}_percentile"],
                    row["year"]
                )
            )

    conn.commit()

    conn.close()

    print("Peer percentile data saved successfully.")

if __name__ == "__main__":

    create_peer_percentiles_table()

    df = prepare_peer_dataframe()

    all_percentiles = []

    peer_groups = df["peer_group_name"].dropna().unique()

    print("\nPeer Groups Found:", len(peer_groups))

    for group in peer_groups:

        peer_df = df[
            df["peer_group_name"] == group
        ].copy()

        print("\n" + "=" * 60)
        print(group)
        print("=" * 60)

        for metric in metrics:

            inverse = metric == "debt_to_equity"

            peer_df[f"{metric}_percentile"] = calculate_percentile(
                peer_df[metric],
                inverse=inverse
            )

        print(
            peer_df[
                [
                    "company_id",
                    "return_on_equity_pct_percentile",
                    "debt_to_equity_percentile",
                    "free_cash_flow_cr_percentile"
                ]
            ]
        )

        all_percentiles.append(peer_df)

    percentile_df = pd.concat(
        all_percentiles,
        ignore_index=True
    )

    print("\nCombined Data:")
    print(percentile_df.head())

    print("\nTotal Companies in Peer Groups:", len(percentile_df))

    save_peer_percentiles(percentile_df)

    