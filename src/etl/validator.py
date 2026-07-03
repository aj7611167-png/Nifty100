import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"


def run_validation():

    conn = sqlite3.connect(DB_PATH)

    failures = []

    print("=" * 50)
    print("DQ-01: Company ID uniqueness")

    q = """
    SELECT id, COUNT(*) AS duplicates
    FROM companies
    GROUP BY id
    HAVING COUNT(*) > 1
    """

    df = pd.read_sql(q, conn)

    if df.empty:
        print("PASS")
    else:
        print("FAIL")
        df["rule"] = "DQ-01"
        df["table"] = "companies"
        failures.append(df)

    print("=" * 50)
    print("DQ-02: (company_id, year) uniqueness")

    tables = [
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "market_cap"
    ]

    for table in tables:

        q = f"""
        SELECT
            company_id,
            year,
            COUNT(*) AS duplicates
        FROM {table}
        GROUP BY company_id, year
        HAVING COUNT(*) > 1
        """

        df = pd.read_sql(q, conn)

        if df.empty:
            print(table, "PASS")
        else:
            print(table, "FAIL")
            df["rule"] = "DQ-02"
            df["table"] = table
            failures.append(df)

    print("=" * 50)
    print("DQ-03: Foreign Key Check")

    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_key_check")

    rows = cursor.fetchall()

    if len(rows) == 0:
        print("PASS")
    else:
        print("FAIL")

        fk = pd.DataFrame(
            rows,
            columns=["table", "rowid", "parent", "fkid"]
        )

        fk["rule"] = "DQ-03"

        failures.append(fk)

    conn.close()

    if failures:
        report = pd.concat(failures, ignore_index=True)
        report.to_csv(
            "output/validation_failures.csv",
            index=False
        )
        print("\nValidation report written to output/validation_failures.csv")
    else:
        print("\nNo validation failures found.")


if __name__ == "__main__":
    run_validation()