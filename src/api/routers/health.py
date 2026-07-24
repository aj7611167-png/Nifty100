import time

from fastapi import APIRouter

from src.api.database import get_connection
from src.api.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])

START_TIME = time.time()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check whether the API is running successfully."
)
def health():
    conn = get_connection()

    tables = [
        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "market_cap",
        "peer_groups",
        "peer_percentiles",
        "documents",
        "stock_prices",
    ]

    db_row_counts = {}

    for table in tables:
        try:
            count = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]
            db_row_counts[table] = count
        except Exception:
            db_row_counts[table] = 0

    conn.close()

    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "db_row_counts": db_row_counts,
    }