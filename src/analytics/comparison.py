import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"


# ==========================================================
# DATABASE
# ==========================================================

def get_connection():
    return sqlite3.connect(DB_PATH)


# ==========================================================
# LOAD TABLES
# ==========================================================

def load_peer_percentiles():

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM peer_percentiles",
        conn
    )

    conn.close()

    return df


def load_peer_groups():

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM peer_groups",
        conn
    )

    conn.close()

    return df


# ==========================================================
# FIND PEER GROUP
# ==========================================================

def get_peer_group(company_id):

    peers = load_peer_groups()

    row = peers[
        peers["company_id"] == company_id
    ]

    if row.empty:
        return None

    return row.iloc[0]["peer_group_name"]


# ==========================================================
# PEER COMPARISON
# ==========================================================

def compare_company(company_id):

    peer_group = get_peer_group(company_id)

    if peer_group is None:
        return None

    percentiles = load_peer_percentiles()

    comparison = percentiles[
        percentiles["peer_group_name"] == peer_group
    ]

    pivot = comparison.pivot(
        index="metric",
        columns="company_id",
        values="percentile_rank"
    )

    return pivot


# ==========================================================
# OVERALL PEER RANKING
# ==========================================================

def rank_peer_group(company_id):

    comparison = compare_company(company_id)

    if comparison is None:
        return None

    ranking = comparison.mean()

    ranking = ranking.reset_index()

    ranking.columns = [
        "company_id",
        "overall_percentile"
    ]

    ranking = ranking.sort_values(
        by="overall_percentile",
        ascending=False
    ).reset_index(drop=True)

    ranking["rank"] = range(
        1,
        len(ranking) + 1
    )

    ranking = ranking[
        [
            "rank",
            "company_id",
            "overall_percentile"
        ]
    ]

    return ranking


# ==========================================================
# BENCHMARK COMPANY
# ==========================================================

def get_benchmark_company(company_id):

    peer_groups = load_peer_groups()

    row = peer_groups[
        peer_groups["company_id"] == company_id
    ]

    if row.empty:
        return None

    peer_group = row.iloc[0]["peer_group_name"]

    benchmark = peer_groups[
        (peer_groups["peer_group_name"] == peer_group) &
        (peer_groups["is_benchmark"] == True)
    ]

    if benchmark.empty:
        return None

    return benchmark.iloc[0]["company_id"]


# ==========================================================
# BENCHMARK COMPARISON
# ==========================================================

def compare_with_benchmark(company_id):

    comparison = compare_company(company_id)

    if comparison is None:
        return None, None

    benchmark = get_benchmark_company(company_id)

    comparison = comparison.T

    comparison["overall_percentile"] = comparison.mean(axis=1)

    benchmark_score = comparison.loc[
        benchmark,
        "overall_percentile"
    ]

    comparison["difference_from_benchmark"] = (
        comparison["overall_percentile"] - benchmark_score
    )

    comparison = comparison.sort_values(
        by="overall_percentile",
        ascending=False
    )

    return benchmark, comparison


# ==========================================================
# MAIN (Testing Only)
# ==========================================================

if __name__ == "__main__":

    company = "INFY"

    print(f"\nPeer Group : {get_peer_group(company)}")

    comparison = compare_company(company)

    print("\nPeer Comparison\n")
    print(comparison)

    ranking = rank_peer_group(company)

    print("\nOverall Peer Ranking\n")
    print(ranking)

    benchmark, benchmark_df = compare_with_benchmark(company)

    print("\nBenchmark Company :", benchmark)

    print("\nBenchmark Comparison\n")

    print(
        benchmark_df[
            [
                "overall_percentile",
                "difference_from_benchmark"
            ]
        ]
    )