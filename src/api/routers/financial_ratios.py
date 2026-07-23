from fastapi import APIRouter, Query
from src.api.database import get_connection
from src.api.schemas.financial_ratio import FinancialRatioResponse

router = APIRouter(
    prefix="/financial-ratios",
    tags=["Financial Ratios"]
)


@router.get(
    "",
    response_model=list[FinancialRatioResponse],
    summary="Get Financial Ratios",
    description="Retrieve financial ratios with optional filtering by company and year."
)
def get_financial_ratios(
    company_id: str | None = Query(
        None,
        description="Filter by company ID"
    ),
    year: str | None = Query(
        None,
        description="Filter by financial year"
    ),
):

    conn = get_connection()

    query = """
    SELECT
        company_id,
        year,
        net_profit_margin_pct,
        operating_profit_margin_pct,
        return_on_equity_pct,
        debt_to_equity,
        interest_coverage,
        asset_turnover,
        free_cash_flow_cr,
        capex_cr,
        earnings_per_share,
        book_value_per_share,
        dividend_payout_ratio_pct,
        total_debt_cr,
        cash_from_operations_cr,
        revenue_cagr_5yr,
        revenue_cagr_5yr_flag,
        pat_cagr_5yr,
        pat_cagr_5yr_flag,
        eps_cagr_5yr,
        eps_cagr_5yr_flag,
        composite_quality_score
    FROM financial_ratios
    WHERE 1=1
    """

    params = []

    if company_id:
        query += " AND company_id = ?"
        params.append(company_id)

    if year:
        query += " AND year = ?"
        params.append(year)

    cursor = conn.execute(query, params)

    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return rows