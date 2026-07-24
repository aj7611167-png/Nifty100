from fastapi import APIRouter, HTTPException
from src.api.database import get_connection

router = APIRouter()


@router.get("/peers/group/{group_name}")
def peer_group(group_name: str):
    conn = get_connection()

    try:
        # Check whether the peer group exists
        exists = conn.execute(
            """
            SELECT 1
            FROM peer_groups
            WHERE TRIM(peer_group_name) = TRIM(?)
            LIMIT 1
            """,
            (group_name,),
        ).fetchone()

        if not exists:
            raise HTTPException(
                status_code=404,
                detail=f"Peer group '{group_name}' not found",
            )

        query = """
        SELECT
            pg.peer_group_name,
            pg.company_id,
            TRIM(c.company_name) AS company_name,
            pg.is_benchmark,
            pp.metric,
            pp.value,
            pp.percentile_rank,
            pp.year
        FROM peer_groups pg
        JOIN companies c
            ON TRIM(pg.company_id) = TRIM(c.id)
        LEFT JOIN peer_percentiles pp
            ON TRIM(pg.company_id) = TRIM(pp.company_id)
           AND TRIM(pg.peer_group_name) = TRIM(pp.peer_group_name)
        WHERE TRIM(pg.peer_group_name) = TRIM(?)
        ORDER BY
            c.company_name,
            pp.metric
        """

        rows = conn.execute(query, (group_name,)).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


@router.get("/peers/company/{company_id}")
def get_peers(company_id: str):
    conn = get_connection()

    try:
        # Find the company's peer group
        company = conn.execute(
            """
            SELECT
                c.id,
                TRIM(c.company_name) AS company_name,
                pg.peer_group_name
            FROM companies c
            JOIN peer_groups pg
                ON TRIM(c.id) = TRIM(pg.company_id)
            WHERE UPPER(TRIM(c.id)) = UPPER(TRIM(?))
            LIMIT 1
            """,
            (company_id,),
        ).fetchone()

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Company not found",
            )

        peer_group = company["peer_group_name"]

        # Fetch peers in same group except the selected company
        rows = conn.execute(
            """
            SELECT
                c.id,
                TRIM(c.company_name) AS company_name,
                pg.peer_group_name,
                pg.is_benchmark
            FROM peer_groups pg
            JOIN companies c
                ON TRIM(pg.company_id) = TRIM(c.id)
            WHERE TRIM(pg.peer_group_name) = TRIM(?)
              AND UPPER(TRIM(c.id)) != UPPER(TRIM(?))
            ORDER BY
                c.company_name
            """,
            (peer_group, company_id),
        ).fetchall()

        return {
            "company": dict(company),
            "peer_group": peer_group,
            "peers": [dict(row) for row in rows],
        }

    finally:
        conn.close()