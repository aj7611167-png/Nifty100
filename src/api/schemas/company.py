from pydantic import BaseModel


class CompanyResponse(BaseModel):
    id: str
    company_logo: str | None
    company_name: str
    chart_link: str | None
    about_company: str | None
    website: str | None
    face_value: float | None
    book_value: float | None
    roe_percentage: float | None
    roce_percentage: float | None
    broad_sector: str | None
    sub_sector: str | None
    market_cap_category: str | None