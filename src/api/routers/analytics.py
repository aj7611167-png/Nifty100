from fastapi import APIRouter, Query
from src.api.database import get_connection

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


def run_query(query: str, limit: int):
    conn = get_connection()

    cursor = conn.execute(query, (limit,))
    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return rows


@router.get("/top-roe")
def top_roe(
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
        return_on_equity_pct
    FROM financial_ratios
    WHERE return_on_equity_pct IS NOT NULL
      AND return_on_equity_pct BETWEEN 0 AND 100
    ORDER BY return_on_equity_pct DESC
    LIMIT ?
    """

    return run_query(query, limit)


@router.get("/top-revenue-cagr")
def top_revenue_cagr(
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
        revenue_cagr_5yr
    FROM financial_ratios
    WHERE revenue_cagr_5yr IS NOT NULL
    ORDER BY revenue_cagr_5yr DESC
    LIMIT ?
    """

    return run_query(query, limit)


@router.get("/top-quality-score")
def top_quality_score(
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
        composite_quality_score
    FROM financial_ratios
    WHERE composite_quality_score IS NOT NULL
    ORDER BY composite_quality_score DESC
    LIMIT ?
    """

    return run_query(query, limit)


@router.get("/top-eps-cagr")
def top_eps_cagr(
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
        eps_cagr_5yr
    FROM financial_ratios
    WHERE eps_cagr_5yr IS NOT NULL
    ORDER BY eps_cagr_5yr DESC
    LIMIT ?
    """

    return run_query(query, limit)


@router.get("/top-pat-cagr")
def top_pat_cagr(
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
        pat_cagr_5yr
    FROM financial_ratios
    WHERE pat_cagr_5yr IS NOT NULL
    ORDER BY pat_cagr_5yr DESC
    LIMIT ?
    """

    return run_query(query, limit)


@router.get("/top-free-cash-flow")
def top_free_cash_flow(
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
        free_cash_flow_cr
    FROM financial_ratios
    WHERE free_cash_flow_cr IS NOT NULL
    ORDER BY free_cash_flow_cr DESC
    LIMIT ?
    """

    return run_query(query, limit)


@router.get("/top-dividend-payout")
def top_dividend_payout(
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
        dividend_payout_ratio_pct
    FROM financial_ratios
    WHERE dividend_payout_ratio_pct IS NOT NULL
    ORDER BY dividend_payout_ratio_pct DESC
    LIMIT ?
    """

    return run_query(query, limit)

@router.get("/top-growth-stocks")
def top_growth_stocks(
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
        revenue_cagr_5yr,
        pat_cagr_5yr,
        eps_cagr_5yr
    FROM financial_ratios
    WHERE revenue_cagr_5yr IS NOT NULL
      AND pat_cagr_5yr IS NOT NULL
      AND eps_cagr_5yr IS NOT NULL
    ORDER BY
        revenue_cagr_5yr DESC,
        pat_cagr_5yr DESC,
        eps_cagr_5yr DESC
    LIMIT ?
    """

    return run_query(query, limit)

@router.get("/top-net-profit-margin")
def top_net_profit_margin(
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
        net_profit_margin_pct
    FROM financial_ratios
    WHERE net_profit_margin_pct IS NOT NULL
      AND net_profit_margin_pct BETWEEN 0 AND 100
    ORDER BY net_profit_margin_pct DESC
    LIMIT ?
    """

    return run_query(query, limit)

@router.get("/top-operating-profit-margin")
def top_operating_profit_margin(
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
        operating_profit_margin_pct
    FROM financial_ratios
    WHERE operating_profit_margin_pct IS NOT NULL
      AND operating_profit_margin_pct BETWEEN 0 AND 100
    ORDER BY operating_profit_margin_pct DESC
    LIMIT ?
    """

    return run_query(query, limit)

@router.get("/company-scorecard")
def company_scorecard(
    company_id: str = Query(
        ...,
        description="Company ID (Example: ABB)"
    )
):

    conn = get_connection()

    query = """
    SELECT
        company_id,
        year,
        return_on_equity_pct,
        revenue_cagr_5yr,
        pat_cagr_5yr,
        eps_cagr_5yr,
        composite_quality_score,
        net_profit_margin_pct,
        operating_profit_margin_pct,
        debt_to_equity,
        free_cash_flow_cr
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year DESC
    LIMIT 1
    """

    cursor = conn.execute(query, (company_id,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return {
            "message": "Company not found"
        }

    return dict(row)

@router.get("/compare")
def compare_companies(
    company1: str = Query(
        ...,
        description="First company ID"
    ),
    company2: str = Query(
        ...,
        description="Second company ID"
    ),
):

    conn = get_connection()

    query = """
    SELECT
        company_id,
        year,
        return_on_equity_pct,
        revenue_cagr_5yr,
        pat_cagr_5yr,
        eps_cagr_5yr,
        composite_quality_score,
        net_profit_margin_pct,
        operating_profit_margin_pct,
        debt_to_equity,
        free_cash_flow_cr
    FROM financial_ratios
    WHERE company_id = ?
      AND year = 'Mar 2024'
    """

    company1_data = conn.execute(query, (company1,)).fetchone()
    company2_data = conn.execute(query, (company2,)).fetchone()

    conn.close()

    return {
        "company1": dict(company1_data) if company1_data else None,
        "company2": dict(company2_data) if company2_data else None,
    }

@router.get("/rankings")
def rankings(
    metric: str = Query(
        ...,
        description="Metric to rank by"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of companies to return"
    )
):

    # Allowed metrics
    valid_metrics = {
        "return_on_equity_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "composite_quality_score",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "free_cash_flow_cr",
        "dividend_payout_ratio_pct",
        "debt_to_equity",
    }

    if metric not in valid_metrics:
        return {
            "error": "Invalid metric",
            "available_metrics": sorted(valid_metrics)
        }

    query = f"""
    SELECT
        company_id,
        year,
        {metric} AS value
    FROM financial_ratios
    WHERE {metric} IS NOT NULL
    """

    # Filter unrealistic percentages
    if metric in {
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
    }:
        query += f"""
        AND {metric} BETWEEN 0 AND 100
        """

    query += f"""
    ORDER BY {metric} DESC
    LIMIT ?
    """

    return run_query(query, limit)

@router.get("/screen-stocks")
def screen_stocks(
    min_roe: float = Query(
        20,
        description="Minimum Return on Equity (%)"
    ),
    max_debt_to_equity: float = Query(
        0.5,
        description="Maximum Debt to Equity"
    ),
    min_quality_score: int = Query(
        20,
        description="Minimum Composite Quality Score"
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
        debt_to_equity,
        revenue_cagr_5yr,
        composite_quality_score
    FROM financial_ratios
    WHERE
        return_on_equity_pct IS NOT NULL
        AND debt_to_equity IS NOT NULL
        AND composite_quality_score IS NOT NULL
        AND return_on_equity_pct >= ?
        AND debt_to_equity <= ?
        AND composite_quality_score >= ?
    ORDER BY
        composite_quality_score DESC,
        return_on_equity_pct DESC
    LIMIT ?
    """

    cursor = conn.execute(
        query,
        (
            min_roe,
            max_debt_to_equity,
            min_quality_score,
            limit
        )
    )

    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return rows