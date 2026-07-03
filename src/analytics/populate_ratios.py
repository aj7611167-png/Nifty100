import sqlite3

from src.analytics.cagr import calculate_cagr

DB = "db/nifty100.db"


def populate():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    companies = cur.execute("""
        SELECT DISTINCT company_id
        FROM profitandloss
        ORDER BY company_id
    """).fetchall()

    print(f"Total companies: {len(companies)}\n")

    for company_row in companies:

        company = company_row["company_id"]

        rows = cur.execute("""
            SELECT
                company_id,
                year,
                sales,
                net_profit,
                eps
            FROM profitandloss
            WHERE company_id = ?
            ORDER BY year
        """, (company,)).fetchall()

        # Remove TTM rows
        rows = [r for r in rows if r["year"] != "TTM"]

        # Need at least 6 yearly records
        if len(rows) < 6:
            print(f"{company:<15} Skipped (only {len(rows)} years)")
            continue

        start = rows[-6]
        end = rows[-1]

        latest_year = end["year"]

        # ---------------- Revenue CAGR ----------------

        if start["sales"] is None or end["sales"] is None:
            revenue_cagr = None
            revenue_flag = "MISSING_DATA"
        else:
            revenue_cagr, revenue_flag = calculate_cagr(
                start["sales"],
                end["sales"],
                5
            )

        # ---------------- PAT CAGR ----------------

        if start["net_profit"] is None or end["net_profit"] is None:
            pat_cagr = None
            pat_flag = "MISSING_DATA"
        else:
            pat_cagr, pat_flag = calculate_cagr(
                start["net_profit"],
                end["net_profit"],
                5
            )

        # ---------------- EPS CAGR ----------------

        if start["eps"] is None or end["eps"] is None:
            eps_cagr = None
            eps_flag = "MISSING_DATA"
        else:
            eps_cagr, eps_flag = calculate_cagr(
                start["eps"],
                end["eps"],
                5
            )

        print(
            f"{company:<15}"
            f" Revenue:{revenue_cagr}"
            f" PAT:{pat_cagr}"
            f" EPS:{eps_cagr}"
        )

        # ---------------- Update Database ----------------

        cur.execute("""
            UPDATE financial_ratios
            SET
                revenue_cagr_5yr = ?,
                revenue_cagr_5yr_flag = ?,
                pat_cagr_5yr = ?,
                pat_cagr_5yr_flag = ?,
                eps_cagr_5yr = ?,
                eps_cagr_5yr_flag = ?
            WHERE company_id = ?
            AND year = ?
        """, (
            revenue_cagr,
            revenue_flag,
            pat_cagr,
            pat_flag,
            eps_cagr,
            eps_flag,
            company,
            latest_year
        ))

    # Commit all updates once
    conn.commit()

    print("\nAll companies updated successfully!")

    conn.close()


if __name__ == "__main__":
    populate()