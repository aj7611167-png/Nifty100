from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/portfolio/stats")
def portfolio():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) as companies,
            AVG(roe_percentage) as avg_roe,
            AVG(roce_percentage) as avg_roce
        FROM companies
    """)

    row = cursor.fetchone()

    conn.close()

    return {
        "companies": row["companies"],
        "average_roe": round(row["avg_roe"], 2),
        "average_roce": round(row["avg_roce"], 2)
    }