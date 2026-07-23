from fastapi import APIRouter, HTTPException
from src.api.database import get_connection

router = APIRouter(tags=["Valuation"])


@router.get("/market-cap", summary="Get Market Cap")
def get_market_cap():
    conn = get_connection()

    try:
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
            ORDER BY company_id ASC, year DESC
        """)

        return [dict(row) for row in cursor.fetchall()]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conn.close()