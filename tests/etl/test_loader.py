from pathlib import Path

from src.etl.loader import RAW_DATA_DIR, FILES


def test_raw_data_directory_exists():
    assert RAW_DATA_DIR.exists()


def test_total_excel_files():
    assert len(FILES) == 12


def test_companies_file_present():
    assert "companies.xlsx" in FILES


def test_profitandloss_file_present():
    assert "profitandloss.xlsx" in FILES


def test_balancesheet_file_present():
    assert "balancesheet.xlsx" in FILES


def test_cashflow_file_present():
    assert "cashflow.xlsx" in FILES


def test_analysis_file_present():
    assert "analysis.xlsx" in FILES


def test_documents_file_present():
    assert "documents.xlsx" in FILES


def test_header_row_companies():
    assert FILES["companies.xlsx"] == 1


def test_header_row_market_cap():
    assert FILES["market_cap.xlsx"] == 0