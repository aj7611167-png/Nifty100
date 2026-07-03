from src.analytics.cagr import (
    calculate_cagr,
    calculate_window,
)


def test_cagr_normal():

    value, flag = calculate_cagr(
        100,
        200,
        3
    )

    assert value == 25.99
    assert flag is None


def test_turnaround():

    value, flag = calculate_cagr(
        -100,
        200,
        3
    )

    assert value is None
    assert flag == "TURNAROUND"


def test_decline_to_loss():

    value, flag = calculate_cagr(
        100,
        -200,
        3
    )

    assert value is None
    assert flag == "DECLINE_TO_LOSS"


def test_both_negative():

    value, flag = calculate_cagr(
        -100,
        -200,
        3
    )

    assert value is None
    assert flag == "BOTH_NEGATIVE"


def test_zero_base():

    value, flag = calculate_cagr(
        0,
        100,
        3
    )

    assert value is None
    assert flag == "ZERO_BASE"


def test_insufficient_years():

    value, flag = calculate_cagr(
        100,
        200,
        0
    )

    assert value is None
    assert flag == "INSUFFICIENT"


def test_window_normal():

    value, flag = calculate_window(
        [100, 110, 150, 200],
        3
    )

    assert value == 25.99
    assert flag is None


def test_window_insufficient():

    value, flag = calculate_window(
        [100, 120],
        5
    )

    assert value is None
    assert flag == "INSUFFICIENT"


def test_same_value():

    value, flag = calculate_cagr(
        100,
        100,
        5
    )

    assert value == 0.0
    assert flag is None


def test_growth_large():

    value, flag = calculate_cagr(
        100,
        400,
        5
    )

    assert value > 30
    assert flag is None