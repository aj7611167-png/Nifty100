from fastapi import APIRouter, Query, HTTPException

from src.api.database import get_connection
from src.api.schemas.screener import ScreenerResponse

router = APIRouter(
    prefix="/screener",
    tags=["Screener"]
)


@router.get(
    "",
    response_model=list[ScreenerResponse],
    summary="Financial Screener",
    description="Screen companies using financial filters."
)
def financial_screener(
    min_roe: float | None = Query(None),
    max_de: float | None = Query(None),
    min_fcf: float | None = Query(None),
    sector: str | None = Query(None),
    min_rev_cagr_5yr: float | None = Query(None),
    min_pat_cagr_5yr: float | None = Query(None),
    max_pe: float | None = Query(None),
):
    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,

        fr.return_on_equity_pct AS roe,

        fr.debt_to_equity,

        fr.free_cash_flow_cr AS free_cash_flow,

        fr.revenue_cagr_5yr,

        fr.pat_cagr_5yr,

        mc.pe_ratio,

        NULL AS composite_quality_score
    FROM companies c

    JOIN (
        SELECT *
        FROM financial_ratios fr1
        WHERE fr1.year = (
            SELECT MAX(fr2.year)
            FROM financial_ratios fr2
            WHERE fr2.company_id = fr1.company_id
        )
    ) fr
    ON c.id = fr.company_id

    LEFT JOIN sectors s
    ON c.id = s.company_id

    LEFT JOIN (
        SELECT *
        FROM market_cap mc1
        WHERE mc1.year = (
            SELECT MAX(mc2.year)
            FROM market_cap mc2
            WHERE mc2.company_id = mc1.company_id
        )
    ) mc
    ON c.id = mc.company_id

    WHERE 1=1
    """

    params = []

    if min_roe is not None:
        query += " AND fr.return_on_equity_pct >= ?"
        params.append(min_roe)

    if max_de is not None:
        query += " AND fr.debt_to_equity <= ?"
        params.append(max_de)

    if min_fcf is not None:
        query += " AND fr.free_cash_flow_cr >= ?"
        params.append(min_fcf)

    if sector:
        query += " AND s.broad_sector = ?"
        params.append(sector)

    if min_rev_cagr_5yr is not None:
        query += " AND fr.revenue_cagr_5yr >= ?"
        params.append(min_rev_cagr_5yr)

    if min_pat_cagr_5yr is not None:
        query += " AND fr.pat_cagr_5yr >= ?"
        params.append(min_pat_cagr_5yr)

    if max_pe is not None:
        query += " AND mc.pe_ratio <= ?"
        params.append(max_pe)

    try:
        cursor = conn.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
