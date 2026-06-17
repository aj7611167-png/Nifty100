from src.etl.normaliser import normalize_year
from src.etl.normaliser import normalize_ticker


def test_year_2024():
    assert normalize_year("FY 2024") == 2024


def test_year_2023():
    assert normalize_year("2023") == 2023


def test_year_none():
    assert normalize_year(None) is None


def test_ticker_upper():
    assert normalize_ticker("tcs") == "TCS"


def test_ticker_ns():
    assert normalize_ticker("reliance.ns") == "RELIANCE"