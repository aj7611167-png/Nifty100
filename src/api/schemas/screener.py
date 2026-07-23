from pydantic import BaseModel


class ScreenerResponse(BaseModel):
    id: str
    company_name: str
    broad_sector: str | None

    roe: float | None
    debt_to_equity: float | None
    free_cash_flow: float | None

    revenue_cagr_5yr: float | None
    pat_cagr_5yr: float | None

    pe_ratio: float | None

    composite_quality_score: float | None