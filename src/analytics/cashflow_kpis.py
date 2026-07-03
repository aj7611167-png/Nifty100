def free_cash_flow(operating_activity, investing_activity):
    return round(operating_activity + investing_activity, 2)


def cfo_quality_score(cfo_list, pat_list):

    if len(cfo_list) == 0 or len(pat_list) == 0:
        return None

    ratios = []

    for cfo, pat in zip(cfo_list, pat_list):

        if pat == 0:
            continue

        ratios.append(cfo / pat)

    if len(ratios) == 0:
        return None

    avg = sum(ratios) / len(ratios)

    if avg > 1:
        return "High Quality"

    if avg >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(investing_activity, sales):

    if sales == 0:
        return None, None

    value = abs(investing_activity) / sales * 100
    value = round(value, 2)

    if value < 3:
        label = "Asset Light"

    elif value <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return value, label


def fcf_conversion_rate(fcf, operating_profit):

    if operating_profit == 0:
        return None

    return round((fcf / operating_profit) * 100, 2)


def capital_allocation_pattern(cfo, cfi, cff):

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    mapping = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "+", "-"): "Liquidating Assets",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "-"): "Pre-Revenue",
        ("+", "-", "+"): "Mixed",
    }

    return mapping.get(signs, "Unknown")