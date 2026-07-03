from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern,
)


def test_free_cash_flow():

    assert (
        free_cash_flow(
            100,
            -40
        )
        == 60
    )


def test_free_cash_flow_negative():

    assert (
        free_cash_flow(
            50,
            -120
        )
        == -70
    )


def test_cfo_quality_high():

    result = cfo_quality_score(
        [100, 120, 150],
        [80, 90, 100]
    )

    assert result == "High Quality"


def test_cfo_quality_moderate():

    result = cfo_quality_score(
        [50, 60],
        [100, 100]
    )

    assert result == "Moderate"


def test_cfo_quality_low():

    result = cfo_quality_score(
        [20, 30],
        [100, 100]
    )

    assert result == "Accrual Risk"


def test_capex_intensity():

    value, label = capex_intensity(
        -50,
        1000
    )

    assert value == 5
    assert label == "Moderate"


def test_capex_zero_sales():

    value, label = capex_intensity(
        -50,
        0
    )

    assert value is None
    assert label is None


def test_fcf_conversion():

    assert (
        fcf_conversion_rate(
            200,
            400
        )
        == 50
    )


def test_fcf_conversion_zero():

    assert (
        fcf_conversion_rate(
            200,
            0
        )
        is None
    )


def test_reinvestor():

    assert (
        capital_allocation_pattern(
            100,
            -100,
            -50
        )
        == "Reinvestor"
    )


def test_distress():

    assert (
        capital_allocation_pattern(
            -100,
            100,
            100
        )
        == "Distress Signal"
    )


def test_cash_accumulator():

    assert (
        capital_allocation_pattern(
            100,
            50,
            20
        )
        == "Cash Accumulator"
    )