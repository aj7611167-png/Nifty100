from pydantic import BaseModel


class BalanceSheetResponse(BaseModel):
    year: str
    equity_capital: float | None
    reserves: int | None
    borrowings: int | None
    other_liabilities: int | None
    total_liabilities: int | None
    fixed_assets: int | None
    cwip: int | None
    investments: int | None
    other_asset: int | None
    total_assets: int | None