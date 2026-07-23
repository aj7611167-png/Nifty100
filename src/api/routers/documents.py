from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter(tags=["Documents"])


@router.get("/documents", summary="Get Annual Reports")
def get_documents():
    conn = get_connection()

    try:
        cursor = conn.execute("""
            SELECT
                company_id,
                Year,
                Annual_Report
            FROM documents
            ORDER BY company_id ASC, Year DESC
        """)

        rows = [dict(row) for row in cursor.fetchall()]
        return rows

    finally:
        conn.close()