from pathlib import Path

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import FileResponse

from src.api.database import get_connection

from src.api.schemas.company import CompanyResponse
from src.api.schemas.company_profile import CompanyProfile
from src.api.schemas.profitandloss import ProfitAndLossResponse
from src.api.schemas.balancesheet import BalanceSheetResponse
from src.api.schemas.cashflow import CashflowResponse
from src.api.schemas.ratios import FinancialRatioResponse

router = APIRouter(prefix="/companies",tags=["Companies"])

@router.get(
    "",
    response_model=list[CompanyResponse],
    summary="Get Companies",
    description="Retrieve all companies with optional filtering by sector, market cap category, and search keyword."
)
def get_companies(
    sector: str | None = Query(
        None,
        description="Filter companies by broad sector",
        examples=["Healthcare"]
    ),
    market_cap_category: str | None = Query(
        None,
        description="Filter by market capitalization category",
        examples=["Large Cap"]
    ),
    search: str | None = Query(
        None,
        description="Search by company ID or company name",
        examples=["ABB"]
    ),
):

    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_logo,
        c.company_name,
        c.chart_link,
        c.about_company,
        c.website,
        c.face_value,
        c.book_value,
        c.roe_percentage,
        c.roce_percentage,
        s.broad_sector,
        s.sub_sector,
        s.market_cap_category
    FROM companies c
    LEFT JOIN sectors s
    ON c.id = s.company_id
    WHERE 1=1
    """

    params = []

    if sector:
        query += " AND s.broad_sector = ?"
        params.append(sector)

    if market_cap_category:
        query += " AND s.market_cap_category = ?"
        params.append(market_cap_category)

    if search:
        query += " AND (c.company_name LIKE ? OR c.id LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    cursor = conn.execute(query, params)

    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return rows

@router.get(
    "/{ticker}",
    response_model=CompanyProfile,
    summary="Company Profile",
    description="Returns full company profile with latest financial ratios."
)
def get_company_profile(ticker: str):

    conn = get_connection()

    query = """
    SELECT

        c.id,
        c.company_logo,
        c.company_name,
        c.chart_link,
        c.about_company,
        c.website,
        c.nse_profile,
        c.bse_profile,
        c.face_value,
        c.book_value,
        c.roe_percentage,
        c.roce_percentage,

        s.broad_sector,
        s.sub_sector,
        s.market_cap_category,

        fr.year,
        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.operating_profit_margin_pct,
        fr.net_profit_margin_pct,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,
        fr.eps_cagr_5yr,
        fr.composite_quality_score

    FROM companies c

    LEFT JOIN sectors s
        ON c.id = s.company_id

    LEFT JOIN financial_ratios fr
        ON c.id = fr.company_id

    WHERE c.id = ?

    ORDER BY fr.year DESC

    LIMIT 1
    """

    row = conn.execute(query, (ticker.upper(),)).fetchone()

    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return dict(row)

@router.get(
    "/{ticker}/pl",
    response_model=list[ProfitAndLossResponse],
    summary="Profit & Loss History",
    description="Returns Profit & Loss history for a company."
)
def get_profit_and_loss(
    ticker: str,
    from_year: str | None = Query(
        None,
        description="Start year (e.g. Mar 2019)"
    ),
    to_year: str | None = Query(
        None,
        description="End year (e.g. Mar 2024)"
    ),
):
    conn = get_connection()

    # Check company exists
    exists = conn.execute(
        "SELECT 1 FROM companies WHERE id = ?",
        (ticker,)
    ).fetchone()

    if not exists:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    query = """
    SELECT
        year,
        sales,
        expenses,
        operating_profit,
        opm_percentage,
        other_income,
        interest,
        depreciation,
        profit_before_tax,
        tax_percentage,
        net_profit,
        eps,
        dividend_payout
    FROM profitandloss
    WHERE company_id = ?
    """

    params = [ticker]

    if from_year:
        query += " AND year >= ?"
        params.append(from_year)

    if to_year:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year"

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [dict(row) for row in rows]

@router.get(
    "/{ticker}/bs",
    response_model=list[BalanceSheetResponse],
    summary="Balance Sheet History",
    description="Returns Balance Sheet history for a company."
)
def get_balance_sheet(
    ticker: str,
    from_year: str | None = Query(
        None,
        description="Start year (e.g. Mar 2019)"
    ),
    to_year: str | None = Query(
        None,
        description="End year (e.g. Mar 2024)"
    ),
):

    conn = get_connection()

    query = """
    SELECT
        year,
        equity_capital,
        reserves,
        borrowings,
        other_liabilities,
        total_liabilities,
        fixed_assets,
        cwip,
        investments,
        other_asset,
        total_assets
    FROM balancesheet
    WHERE company_id = ?
    """

    params = [ticker]

    if from_year:
        query += " AND year >= ?"
        params.append(from_year)

    if to_year:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year"

    cursor = conn.execute(query, params)

    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return rows

@router.get(
    "/{ticker}/cashflow",
    response_model=list[CashflowResponse],
    summary="Cash Flow History",
    description="Returns Cash Flow history for a company."
)
def get_cashflow(
    ticker: str,
    from_year: str | None = Query(
        None,
        description="Start year (e.g. Mar 2019)"
    ),
    to_year: str | None = Query(
        None,
        description="End year (e.g. Mar 2024)"
    ),
):

    conn = get_connection()

    company = conn.execute(
        "SELECT id FROM companies WHERE id=?",
        (ticker,)
    ).fetchone()

    if not company:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    query = """
    SELECT
        year,
        operating_activity,
        investing_activity,
        financing_activity,
        net_cash_flow
    FROM cashflow
    WHERE company_id=?
    """

    params = [ticker]

    if from_year:
        query += " AND year >= ?"
        params.append(from_year)

    if to_year:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year"

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [dict(row) for row in rows]

@router.get(
    "/{ticker}/ratios",
    response_model=list[FinancialRatioResponse],
    summary="Financial Ratios",
    description="Returns computed financial ratios for a company. Optionally filter by year."
)
def get_financial_ratios(
    ticker: str,
    year: str | None = Query(
        None,
        description="Return only a specific year (e.g. Mar 2024)"
    ),
):

    conn = get_connection()

    company = conn.execute(
        "SELECT id FROM companies WHERE id=?",
        (ticker,)
    ).fetchone()

    if not company:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    query = """
    SELECT
        year,
        net_profit_margin_pct,
        operating_profit_margin_pct,
        return_on_equity_pct,
        debt_to_equity,
        interest_coverage,
        asset_turnover,
        free_cash_flow_cr,
        capex_cr,
        earnings_per_share,
        book_value_per_share,
        dividend_payout_ratio_pct,
        total_debt_cr,
        cash_from_operations_cr,
        revenue_cagr_5yr,
        revenue_cagr_5yr_flag,
        pat_cagr_5yr,
        pat_cagr_5yr_flag,
        eps_cagr_5yr,
        eps_cagr_5yr_flag,
        composite_quality_score
    FROM financial_ratios
    WHERE company_id=?
    """

    params = [ticker]

    if year:
        query += " AND year=?"
        params.append(year)

    query += " ORDER BY year"

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [dict(row) for row in rows]

@router.get(
    "/{ticker}/tearsheet",
    summary="Download Company Tearsheet",
    description="Returns the pre-generated PDF tearsheet for a company."
)
def download_tearsheet(ticker: str):
    """
    Download the PDF tearsheet for a company.
    """

    # Verify company exists
    conn = get_connection()

    company = conn.execute(
        "SELECT id FROM companies WHERE id = ?",
        (ticker.upper(),)
    ).fetchone()

    conn.close()

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    # Path to PDF
    pdf_path = (
        Path(__file__).resolve().parents[3]
        / "reports"
        / "tearsheets"
        / f"{ticker.upper()}.pdf"
    )

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Tearsheet PDF not found"
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{ticker.upper()}_tearsheet.pdf"
    )
