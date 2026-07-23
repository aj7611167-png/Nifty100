from pydantic import BaseModel


class CompanyProfile(BaseModel):
    id: str
    company_logo: str | None
    company_name: str
    chart_link: str | None
    about_company: str | None
    website: str | None
    nse_profile: str | None
    bse_profile: str | None
    face_value: float | None
    book_value: float | None
    roe_percentage: float | None
    roce_percentage: float | None

    broad_sector: str | None
    sub_sector: str | None
    market_cap_category: str | None

    year: str | None
    return_on_equity_pct: float | None
    debt_to_equity: float | None
    operating_profit_margin_pct: float | None
    net_profit_margin_pct: float | None
    revenue_cagr_5yr: float | None
    pat_cagr_5yr: float | None
    eps_cagr_5yr: float | None
    composite_quality_score: float | None