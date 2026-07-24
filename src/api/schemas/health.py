from typing import Dict

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float
    db_row_counts: Dict[str, int]