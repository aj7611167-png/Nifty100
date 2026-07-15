# ==========================================================
# STRENGTHS
# ==========================================================

def find_strengths(company):

    strengths = []

    if company["return_on_equity_pct"] >= 20:
        strengths.append("Excellent Return on Equity")

    if company["roce_percentage"] >= 20:
        strengths.append("High Return on Capital Employed")

    if company["debt_to_equity"] <= 0.5:
        strengths.append("Low Debt")

    if company["free_cash_flow_cr"] > 0:
        strengths.append("Positive Free Cash Flow")

    if company["revenue_cagr_5yr"] >= 15:
        strengths.append("Strong Revenue Growth")

    if company["pat_cagr_5yr"] >= 15:
        strengths.append("Strong Profit Growth")

    if company["eps_cagr_5yr"] >= 15:
        strengths.append("Strong EPS Growth")

    if company["dividend_yield_pct"] >= 2:
        strengths.append("Healthy Dividend Yield")

    return strengths

# ==========================================================
# WEAKNESSES
# ==========================================================

def find_weaknesses(company):

    weaknesses = []

    if company["return_on_equity_pct"] < 15:
        weaknesses.append("Low Return on Equity")

    if company["roce_percentage"] < 15:
        weaknesses.append("Low Return on Capital Employed")

    if company["debt_to_equity"] > 1:
        weaknesses.append("High Debt")

    if company["free_cash_flow_cr"] <= 0:
        weaknesses.append("Negative Free Cash Flow")

    if company["revenue_cagr_5yr"] < 10:
        weaknesses.append("Slow Revenue Growth")

    if company["pat_cagr_5yr"] < 10:
        weaknesses.append("Slow Profit Growth")

    if company["eps_cagr_5yr"] < 10:
        weaknesses.append("Slow EPS Growth")

    if company["pe_ratio"] > 40:
        weaknesses.append("Expensive Valuation (High P/E)")

    if company["pb_ratio"] > 5:
        weaknesses.append("Expensive Valuation (High P/B)")

    return weaknesses

# ==========================================================
# INVESTMENT VERDICT
# ==========================================================

def generate_verdict(company):

    strengths = find_strengths(company)
    weaknesses = find_weaknesses(company)

    score = len(strengths) - len(weaknesses)

    if score >= 4:
        return "★★★★★ Excellent Long-Term Compounder"

    elif score >= 2:
        return "★★★★☆ Strong Business"

    elif score >= 0:
        return "★★★☆☆ Average Investment"

    elif score >= -2:
        return "★★☆☆☆ Risky Investment"

    else:
        return "★☆☆☆☆ Avoid"
    


if __name__ == "__main__":

    from src.analytics.report import load_company_data
    from src.analytics.report import get_company

    df = load_company_data()

    company = get_company(df, "TCS")

    strengths = find_strengths(company)
    weaknesses = find_weaknesses(company)
    verdict = generate_verdict(company)

    print("\nStrengths")

    for item in strengths:
        print("✓", item)

    print("\nWeaknesses")

    for item in weaknesses:
        print("•", item)

    print("\nFinal Verdict")
    print(verdict)