from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()

@router.get("/sectors")
def sectors():
    conn = get_connection()

    cursor = conn.execute("""
        SELECT
            broad_sector,
            COUNT(*) AS companies
        FROM sectors
        GROUP BY broad_sector
        ORDER BY companies DESC
    """)

    data = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return data