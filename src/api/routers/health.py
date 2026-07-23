from fastapi import APIRouter

from src.api.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check whether the API is running successfully."
)
def health():
    return {
        "status": "ok",
        "version": "1.0.0"
    }