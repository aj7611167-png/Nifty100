from pydantic import BaseModel


class FinancialRatioResponse(BaseModel):
    year: str

    net_profit_margin_pct: float | None
    operating_profit_margin_pct: float | None
    return_on_equity_pct: float | None
    debt_to_equity: float | None
    interest_coverage: float | None
    asset_turnover: float | None

    free_cash_flow_cr: float | None
    capex_cr: float | None

    earnings_per_share: float | None
    book_value_per_share: float | None
    dividend_payout_ratio_pct: float | None

    total_debt_cr: int | None
    cash_from_operations_cr: float | None

    revenue_cagr_5yr: float | None
    revenue_cagr_5yr_flag: str | None

    pat_cagr_5yr: float | None
    pat_cagr_5yr_flag: str | None

    eps_cagr_5yr: float | None
    eps_cagr_5yr_flag: str | None

    composite_quality_score: float | None