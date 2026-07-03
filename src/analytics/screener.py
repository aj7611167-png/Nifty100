import sqlite3

DB = "db/nifty100.db"


def top_quality_companies(limit=20):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    rows = cur.execute("""
        SELECT
            company_id,
            year,
            composite_quality_score,
            revenue_cagr_5yr,
            pat_cagr_5yr,
            eps_cagr_5yr
        FROM financial_ratios
        WHERE composite_quality_score IS NOT NULL
        ORDER BY composite_quality_score DESC,
                 revenue_cagr_5yr DESC
        LIMIT ?
    """, (limit,)).fetchall()

    print("=" * 90)
    print(
        f"{'Rank':<5}"
        f"{'Company':<15}"
        f"{'Score':<8}"
        f"{'Revenue':<12}"
        f"{'PAT':<12}"
        f"{'EPS':<12}"
    )
    print("=" * 90)

    for rank, row in enumerate(rows, start=1):
        print(
            f"{rank:<5}"
            f"{row['company_id']:<15}"
            f"{row['composite_quality_score']:<8}"
            f"{str(row['revenue_cagr_5yr']):<12}"
            f"{str(row['pat_cagr_5yr']):<12}"
            f"{str(row['eps_cagr_5yr']):<12}"
        )

    conn.close()


if __name__ == "__main__":
    top_quality_companies()