from fastapi import APIRouter, Query
from src.api.database import get_connection

router = APIRouter(
    prefix="/risk",
    tags=["Risk"]
)


def run_query(query: str, limit: int):
    conn = get_connection()

    cursor = conn.execute(query, (limit,))
    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return rows


@router.get("/top-debt-to-equity")
def top_debt_to_equity(
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of companies to return"
    )
):

    query = """
    SELECT
        company_id,
        year,
        debt_to_equity
    FROM financial_ratios
    WHERE debt_to_equity IS NOT NULL
    ORDER BY debt_to_equity DESC
    LIMIT ?
    """

    return run_query(query, limit)

@router.get("/low-debt-companies")
def low_debt_companies(
    max_debt_to_equity: float = Query(
        0.5,
        ge=0,
        description="Maximum Debt to Equity"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of companies to return"
    )
):

    conn = get_connection()

    query = """
    SELECT
        company_id,
        year,
        debt_to_equity
    FROM financial_ratios
    WHERE debt_to_equity IS NOT NULL
      AND debt_to_equity <= ?
    ORDER BY debt_to_equity ASC
    LIMIT ?
    """

    cursor = conn.execute(query, (max_debt_to_equity, limit))
    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return rows

@router.get("/high-roe-low-debt")
def high_roe_low_debt(
    min_roe: float = Query(
        20,
        ge=0,
        description="Minimum Return on Equity (%)"
    ),
    max_debt_to_equity: float = Query(
        0.5,
        ge=0,
        description="Maximum Debt to Equity"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of companies to return"
    )
):

    conn = get_connection()

    query = """
    SELECT
        company_id,
        year,
        return_on_equity_pct,
        debt_to_equity
    FROM financial_ratios
    WHERE return_on_equity_pct IS NOT NULL
      AND debt_to_equity IS NOT NULL
      AND return_on_equity_pct >= ?
      AND debt_to_equity <= ?
    ORDER BY
        return_on_equity_pct DESC,
        debt_to_equity ASC
    LIMIT ?
    """

    cursor = conn.execute(
        query,
        (min_roe, max_debt_to_equity, limit)
    )

    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return rows