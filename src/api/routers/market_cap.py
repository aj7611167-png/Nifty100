from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/market-cap")
def market_cap():
    conn = get_connection()

    cursor = conn.execute("""
        SELECT
            company_id,
            year,
            market_cap_crore,
            enterprise_value_crore,
            pe_ratio,
            pb_ratio,
            ev_ebitda,
            dividend_yield_pct
        FROM market_cap
        LIMIT 100
    """)

    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return rows