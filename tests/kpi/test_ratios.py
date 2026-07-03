from src.analytics.ratios import *


# =====================================================
# DAY 08
# =====================================================

def test_net_profit_margin_normal():
    assert net_profit_margin(100, 1000) == 10


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_net_profit_margin_loss():
    assert net_profit_margin(-50, 1000) == -5


def test_operating_profit_margin():
    assert operating_profit_margin(250, 1000) == 25


def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(200, 0) is None


def test_opm_crosscheck_ok():
    calc = operating_profit_margin(250, 1000)
    assert check_opm_difference(calc, 25) is False


def test_opm_crosscheck_fail():
    calc = operating_profit_margin(250, 1000)
    assert check_opm_difference(calc, 20) is True


def test_roe_normal():
    assert return_on_equity(100, 200, 300) == 20


def test_roe_negative_equity():
    assert return_on_equity(100, -200, 100) is None


def test_roce_normal():
    assert return_on_capital_employed(
        150,
        200,
        300,
        500
    ) == 15


def test_roa_normal():
    assert return_on_assets(120, 600) == 20


def test_roa_zero_assets():
    assert return_on_assets(100, 0) is None


def test_roce_zero_capital():
    assert return_on_capital_employed(
        100,
        0,
        0,
        0
    ) is None


# =====================================================
# DAY 09
# =====================================================

def test_debt_to_equity_normal():
    assert debt_to_equity(500, 200, 300) == 1


def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 100, 200) == 0


def test_debt_to_equity_negative_equity():
    assert debt_to_equity(100, -200, 100) is None


def test_high_leverage_flag():
    assert high_leverage_flag(6, "Industrials") is True


def test_high_leverage_financials():
    assert high_leverage_flag(8, "Financials") is False


def test_interest_coverage_ratio():
    assert interest_coverage_ratio(200, 50, 50) == 5


def test_interest_coverage_zero_interest():
    assert interest_coverage_ratio(100, 20, 0) is None


def test_icr_label():
    assert icr_label(0) == "Debt Free"


def test_icr_warning():
    assert icr_warning_flag(1.2) is True


def test_net_debt():
    assert net_debt(500, 150) == 350


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2


def test_asset_turnover_zero_assets():
    assert asset_turnover(1000, 0) is None