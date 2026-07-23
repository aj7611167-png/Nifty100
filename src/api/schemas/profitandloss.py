from pydantic import BaseModel


class ProfitAndLossResponse(BaseModel):
    year: str
    sales: int | None
    expenses: int | None
    operating_profit: float | None
    opm_percentage: float | None
    other_income: int | None
    interest: int | None
    depreciation: int | None
    profit_before_tax: int | None
    tax_percentage: float | None
    net_profit: int | None
    eps: float | None
    dividend_payout: float | None
    