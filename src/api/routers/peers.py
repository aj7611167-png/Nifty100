from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter(prefix="/peers", tags=["Peers"])


@router.get("")
def peers():

    conn = get_connection()

    query = """
    SELECT
        peer_group_name,
        company_id,
        is_benchmark
    FROM peer_groups
    ORDER BY peer_group_name, company_id
    """

    cursor = conn.execute(query)

    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return rows