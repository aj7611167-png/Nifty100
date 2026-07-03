import sqlite3
import pandas as pd

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    asset_turnover
)

DB_PATH = "db/nifty100.db"


def populate():

    conn = sqlite3.connect(DB_PATH)

    pnl = pd.read_sql(
        """
        SELECT *
        FROM profitandloss
        """,
        conn
    )

    bs = pd.read_sql(
        """
        SELECT *
        FROM balancesheet
        """,
        conn
    )

    if len(pnl) == 0:
        print("profitandloss empty")
        return

    rows = []

    for _, p in pnl.iterrows():

        company = p["company_id"]
        year = p["year"]

        b = bs[
            (bs["company_id"] == company)
            &
            (bs["year"] == year)
        ]

        if len(b) == 0:
            continue

        b = b.iloc[0]

        npm = net_profit_margin(
            p.get("net_profit", 0),
            p.get("sales", 0)
        )

        opm = operating_profit_margin(
            p.get("operating_profit", 0),
            p.get("sales", 0)
        )

        roe = return_on_equity(
            p.get("net_profit", 0),
            b.get("equity_capital", 0),
            b.get("reserves", 0)
        )

        de = debt_to_equity(
            b.get("borrowings", 0),
            b.get("equity_capital", 0),
            b.get("reserves", 0)
        )

        at = asset_turnover(
            p.get("sales", 0),
            b.get("total_assets", 0)
        )

        rows.append([
            company,
            year,
            npm,
            opm,
            roe,
            de,
            at
        ])

    out = pd.DataFrame(
        rows,
        columns=[
            "company_id",
            "year",
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "return_on_equity_pct",
            "debt_to_equity",
            "asset_turnover"
        ]
    )

    out.to_sql(
        "financial_ratios",
        conn,
        if_exists="append",
        index=False
    )

    print("ROWS WRITTEN:", len(out))

    conn.close()


if __name__ == "__main__":
    populate()