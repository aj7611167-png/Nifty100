def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin (%)
    """
    if sales is None or sales == 0:
        return None
    if net_profit is None:
        return None

    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin (%)
    """
    if sales is None or sales == 0:
        return None
    if operating_profit is None:
        return None

    return (operating_profit / sales) * 100


def check_opm_difference(calculated_opm, reported_opm):
    """
    Returns True if difference > 1%
    """
    if calculated_opm is None or reported_opm is None:
        return False

    return abs(calculated_opm - reported_opm) > 1


def return_on_equity(net_profit, equity_capital, reserves):
    """
    ROE (%)
    """
    if net_profit is None:
        return None

    equity = (equity_capital or 0) + (reserves or 0)

    if equity <= 0:
        return None

    roe = (net_profit / equity) * 100

    # Safety clamp to remove insane distortions
    if roe > 200:
        return 200
    if roe < -100:
        return -100

    return roe


def return_on_capital_employed(ebit, equity_capital, reserves, borrowings):
    """
    ROCE (%)
    """
    if ebit is None:
        return None

    capital = (equity_capital or 0) + (reserves or 0) + (borrowings or 0)

    if capital <= 0:
        return None

    roce = (ebit / capital) * 100

    if roce > 200:
        return 200
    if roce < -100:
        return -100

    return roce


def return_on_assets(net_profit, total_assets):
    """
    ROA (%)
    """
    if net_profit is None or total_assets is None:
        return None

    if total_assets == 0:
        return None

    roa = (net_profit / total_assets) * 100

    if roa > 100:
        return 100
    if roa < -100:
        return -100

    return roa


# =====================================================
# LEVERAGE & RISK
# =====================================================

def debt_to_equity(borrowings, equity_capital, reserves):
    """
    Debt / Equity
    """
    borrowings = borrowings or 0
    equity = (equity_capital or 0) + (reserves or 0)

    if borrowings == 0:
        return 0

    if equity <= 0:
        return None

    return borrowings / equity


def high_leverage_flag(de_ratio, broad_sector):
    """
    High leverage if D/E > 5
    except Financials sector
    """
    if de_ratio is None:
        return False

    if broad_sector == "Financials":
        return False

    return de_ratio > 5


def interest_coverage_ratio(operating_profit, other_income, interest):
    """
    Interest Coverage Ratio
    """
    if interest is None or interest == 0:
        return None

    operating_profit = operating_profit or 0
    other_income = other_income or 0

    return (operating_profit + other_income) / interest


def icr_warning_flag(icr):
    """
    Warning if ICR < 1.5
    """
    if icr is None:
        return False

    return icr < 1.5


def net_debt(borrowings, investments):
    """
    Net Debt
    """
    return (borrowings or 0) - (investments or 0)


def asset_turnover(sales, total_assets):
    """
    Asset Turnover
    """
    if sales is None or total_assets is None:
        return None

    if total_assets == 0:
        return None

    return sales / total_assets