import pandas as pd

from src.etl.data_quality import (
    validate_company_id,
    validate_ticker,
    validate_duplicate_company,
    validate_negative_revenue,
    validate_negative_assets,
    validate_negative_profit,
    validate_missing_year,
    validate_duplicate_year,
    validate_negative_cashflow,
    validate_missing_sector,
    validate_missing_company_name,
    validate_negative_equity,
    validate_missing_market_cap,
    validate_duplicate_ticker,
)


def test_dq01_missing_company_id():
    df = pd.DataFrame({"company_id": [None]})
    issues = validate_company_id(df)
    assert issues[0]["rule_id"] == "DQ-01"
    assert issues[0]["severity"] == "HIGH"


def test_dq02_missing_ticker():
    df = pd.DataFrame({"ticker": [None]})
    issues = validate_ticker(df)
    assert issues[0]["rule_id"] == "DQ-02"


def test_dq03_duplicate_company():
    df = pd.DataFrame({"company_id": [1, 1]})
    issues = validate_duplicate_company(df)
    assert issues[0]["rule_id"] == "DQ-03"


def test_dq04_negative_revenue():
    df = pd.DataFrame({"revenue": [-100]})
    issues = validate_negative_revenue(df)
    assert issues[0]["rule_id"] == "DQ-04"


def test_dq05_negative_assets():
    df = pd.DataFrame({"total_assets": [-10]})
    issues = validate_negative_assets(df)
    assert issues[0]["rule_id"] == "DQ-05"


def test_dq06_negative_profit():
    df = pd.DataFrame({"net_profit": [-5]})
    issues = validate_negative_profit(df)
    assert issues[0]["rule_id"] == "DQ-06"


def test_dq07_missing_year():
    df = pd.DataFrame({"year": [None]})
    issues = validate_missing_year(df)
    assert issues[0]["rule_id"] == "DQ-07"


def test_dq08_duplicate_year():
    df = pd.DataFrame(
        {
            "company_id": [1, 1],
            "year": [2024, 2024],
        }
    )
    issues = validate_duplicate_year(df)
    assert issues[0]["rule_id"] == "DQ-08"


def test_dq09_negative_cashflow():
    df = pd.DataFrame({"cash_flow": [-20]})
    issues = validate_negative_cashflow(df)
    assert issues[0]["rule_id"] == "DQ-09"


def test_dq10_missing_sector():
    df = pd.DataFrame({"sector": [None]})
    issues = validate_missing_sector(df)
    assert issues[0]["rule_id"] == "DQ-10"


def test_dq11_missing_company_name():
    df = pd.DataFrame({"company_name": [None]})
    issues = validate_missing_company_name(df)
    assert issues[0]["rule_id"] == "DQ-11"


def test_dq12_negative_equity():
    df = pd.DataFrame({"equity": [-500]})
    issues = validate_negative_equity(df)
    assert issues[0]["rule_id"] == "DQ-12"


def test_dq13_missing_market_cap():
    df = pd.DataFrame({"market_cap": [None]})
    issues = validate_missing_market_cap(df)
    assert issues[0]["rule_id"] == "DQ-13"


def test_dq14_duplicate_ticker():
    df = pd.DataFrame({"ticker": ["TCS", "TCS"]})
    issues = validate_duplicate_ticker(df)
    assert issues[0]["rule_id"] == "DQ-14"