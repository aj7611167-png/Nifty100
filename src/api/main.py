from src.api.routers import (
    health,
    companies,
    screener,
    sectors,
    peers,
    valuation,
    portfolio,
    documents,
    financial_ratios,
    analytics,
    risk,
)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(
    title="NIFTY100 Financial Intelligence API",
    version="1.0.0"
)

# ---------------------------------------
# CORS
# ---------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------
# Request Logging Middleware
# ---------------------------------------

@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()

    response = await call_next(request)

    process_time = time.time() - start

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"{process_time:.3f}s"
    )

    return response


# ---------------------------------------
# Root Endpoint
# ---------------------------------------

@app.get("/")
def root():
    return {
        "message": "NIFTY100 Financial Intelligence API"
    }


# ---------------------------------------
# API Routers
# ---------------------------------------

app.include_router(health.router, prefix="/api/v1")
app.include_router(companies.router, prefix="/api/v1")
app.include_router(screener.router, prefix="/api/v1")
app.include_router(sectors.router, prefix="/api/v1")
app.include_router(peers.router, prefix="/api/v1")
app.include_router(valuation.router, prefix="/api/v1")
app.include_router(portfolio.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(financial_ratios.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(risk.router, prefix="/api/v1")