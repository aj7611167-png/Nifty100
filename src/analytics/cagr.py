import math


def calculate_cagr(beginning, ending, years):
    """
    Returns:
    (cagr_value, flag)

    Example:
    (12.5, None)
    (None, "TURNAROUND")
    """

    if years <= 0:
        return None, "INSUFFICIENT"

    if beginning == 0:
        return None, "ZERO_BASE"

    if beginning < 0 and ending > 0:
        return None, "TURNAROUND"

    if beginning > 0 and ending < 0:
        return None, "DECLINE_TO_LOSS"

    if beginning < 0 and ending < 0:
        return None, "BOTH_NEGATIVE"

    try:
        value = (
            (ending / beginning)
            ** (1 / years)
            - 1
        ) * 100

        return round(value, 2), None

    except Exception:
        return None, "INSUFFICIENT"


def calculate_window(values, years):

    if len(values) < years + 1:
        return None, "INSUFFICIENT"

    start = values[0]
    end = values[years]

    return calculate_cagr(
        start,
        end,
        years
    )