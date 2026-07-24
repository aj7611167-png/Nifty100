from fastapi import APIRouter, HTTPException
from src.api.database import get_connection

router = APIRouter()


@router.get("/sectors")
def sectors():
    conn = get_connection()

    cursor = conn.execute("""
        SELECT
            broad_sector,
            COUNT(*) AS company_count
        FROM sectors
        GROUP BY broad_sector
        ORDER BY company_count DESC
    """)

    data = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return data


@router.get("/sectors/{sector}/companies")
def sector_companies(sector: str):
    conn = get_connection()

    # Accept common aliases
    sector_aliases = {
        "IT": "Information Technology",
        "INFOTECH": "Information Technology",
        "TECH": "Information Technology",
    }

    normalized_sector = sector_aliases.get(sector.upper(), sector)

    query = """
    SELECT
        c.id AS company_id,
        c.company_name,
        s.broad_sector,
        s.sub_sector,
        fr.year,
        fr.return_on_equity_pct,
        fr.operating_profit_margin_pct,
        fr.net_profit_margin_pct,
        fr.debt_to_equity,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,
        fr.eps_cagr_5yr,
        fr.composite_quality_score
    FROM sectors s
    JOIN companies c
        ON s.company_id = c.id
    LEFT JOIN financial_ratios fr
        ON fr.company_id = c.id
    WHERE
        s.broad_sector = ?
        AND fr.year = (
            SELECT MAX(f2.year)
            FROM financial_ratios f2
            WHERE f2.company_id = c.id
        )
    ORDER BY c.company_name
    """

    rows = conn.execute(query, (normalized_sector,)).fetchall()

    conn.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"Sector '{sector}' not found"
        )

    return [dict(row) for row in rows]