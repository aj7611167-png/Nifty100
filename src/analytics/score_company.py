import sqlite3

DB = "db/nifty100.db"


def safe(value):
    """
    Convert None → 0 safely
    """
    if value is None:
        return None
    return float(value)


def metric_score(value):
    """
    Convert CAGR into score out of 10.
    """

    value = safe(value)

    if value is None:
        return 0

    if value >= 25:
        return 10
    elif value >= 20:
        return 9
    elif value >= 15:
        return 8
    elif value >= 12:
        return 7
    elif value >= 10:
        return 6
    elif value >= 8:
        return 5
    elif value >= 5:
        return 4
    elif value >= 0:
        return 2
    else:
        return 0


def score_companies():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    companies = cur.execute("""
        SELECT DISTINCT company_id
        FROM financial_ratios
        ORDER BY company_id
    """).fetchall()

    print(f"Total companies: {len(companies)}\n")

    results = []

    for company_row in companies:
        company = company_row["company_id"]

        row = cur.execute("""
            SELECT
                revenue_cagr_5yr,
                pat_cagr_5yr,
                eps_cagr_5yr
            FROM financial_ratios
            WHERE company_id = ?
            ORDER BY year DESC
            LIMIT 1
        """, (company,)).fetchone()

        if row is None:
            continue

        revenue_score = metric_score(row["revenue_cagr_5yr"])
        pat_score = metric_score(row["pat_cagr_5yr"])
        eps_score = metric_score(row["eps_cagr_5yr"])

        total_score = revenue_score + pat_score + eps_score

        results.append({
            "company": company,
            "score": total_score,
            "revenue": row["revenue_cagr_5yr"],
            "pat": row["pat_cagr_5yr"],
            "eps": row["eps_cagr_5yr"]
        })

    conn.close()

    results.sort(key=lambda x: x["score"], reverse=True)

    print("=" * 75)
    print(f"{'Rank':<5} {'Company':<15} {'Score':<8} {'Revenue':<10} {'PAT':<10} {'EPS':<10}")
    print("=" * 75)

    for rank, c in enumerate(results, start=1):
        print(
            f"{rank:<5}"
            f"{c['company']:<15}"
            f"{c['score']:<8}"
            f"{str(c['revenue']):<10}"
            f"{str(c['pat']):<10}"
            f"{str(c['eps']):<10}"
        )


if __name__ == "__main__":
    score_companies()