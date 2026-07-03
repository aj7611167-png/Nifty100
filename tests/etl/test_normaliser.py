import math
import pytest

from src.etl.normaliser import normalize_year, normalize_ticker


# ==========================================================
# normalize_year Tests
# ==========================================================

@pytest.mark.parametrize(
    "value, expected",
    [
        ("FY 2024", 2024),
        ("2023", 2023),
        ("FY2022", 2022),
        ("2021", 2021),
        (" 2020 ", 2020),
        ("Year 2019", 2019),
        ("Annual Report 2018", 2018),
        ("Financial Year 2017", 2017),
        ("FY 2016", 2016),
        ("2015", 2015),
        ("FY2014", 2014),
        ("Report 2013", 2013),
        ("2012 Data", 2012),
        ("FY 2011", 2011),
        ("2010", 2010),
        ("FY 2022-2023", 2022),
        ("ABC", None),
        ("", None),
        (None, None),
    ],
)
def test_normalize_year(value, expected):
    assert normalize_year(value) == expected


def test_normalize_year_nan():
    assert normalize_year(float("nan")) is None


# ==========================================================
# normalize_ticker Tests
# ==========================================================

@pytest.mark.parametrize(
    "value, expected",
    [
        ("tcs", "TCS"),
        ("reliance.ns", "RELIANCE"),
        ("infy.bo", "INFY"),
        (" hdfcbank ", "HDFCBANK"),
        ("ITC", "ITC"),
        ("adanient.ns", "ADANIENT"),
        ("sbin.ns", "SBIN"),
        ("axisbank.bo", "AXISBANK"),
        ("ltim", "LTIM"),
        ("bajajfinserv.ns", "BAJAJFINSERV"),
        ("ultracemco.bo", "ULTRACEMCO"),
        ("", ""),
        ("123", "123"),
        ("abc123.ns", "ABC123"),
        ("   tcs.ns   ", "TCS"),
        (None, None),
    ],
)
def test_normalize_ticker(value, expected):
    assert normalize_ticker(value) == expected


def test_normalize_ticker_nan():
    assert normalize_ticker(float("nan")) is None