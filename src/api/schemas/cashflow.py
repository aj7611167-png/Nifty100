from pydantic import BaseModel


class CashflowResponse(BaseModel):
    year: str

    operating_activity: float | None
    investing_activity: float | None
    financing_activity: float | None
    net_cash_flow: float | None