import pandas as pd


def _build_issue(rule_id, severity, field, issue, row):
    return {
        "rule_id": rule_id,
        "severity": severity,
        "field": field,
        "issue": issue,
        "row": int(row),
    }


def validate_company_id(df: pd.DataFrame):
    issues = []
    if "company_id" not in df.columns:
        return issues

    for idx in df[df["company_id"].isna()].index:
        issues.append(
            _build_issue(
                "DQ-01",
                "HIGH",
                "company_id",
                "Missing company_id",
                idx,
            )
        )
    return issues


def validate_ticker(df: pd.DataFrame):
    issues = []
    if "ticker" not in df.columns:
        return issues

    for idx in df[df["ticker"].isna()].index:
        issues.append(
            _build_issue(
                "DQ-02",
                "HIGH",
                "ticker",
                "Missing ticker",
                idx,
            )
        )
    return issues


def validate_duplicate_company(df: pd.DataFrame):
    issues = []
    if "company_id" not in df.columns:
        return issues

    dup = df[df.duplicated("company_id", keep=False)]

    for idx in dup.index:
        issues.append(
            _build_issue(
                "DQ-03",
                "HIGH",
                "company_id",
                "Duplicate company_id",
                idx,
            )
        )

    return issues


def validate_negative_revenue(df: pd.DataFrame):
    issues = []

    if "revenue" not in df.columns:
        return issues

    invalid = df[df["revenue"] < 0]

    for idx in invalid.index:
        issues.append(
            _build_issue(
                "DQ-04",
                "HIGH",
                "revenue",
                "Negative revenue",
                idx,
            )
        )

    return issues


def validate_negative_assets(df: pd.DataFrame):
    issues = []

    if "total_assets" not in df.columns:
        return issues

    invalid = df[df["total_assets"] < 0]

    for idx in invalid.index:
        issues.append(
            _build_issue(
                "DQ-05",
                "HIGH",
                "total_assets",
                "Negative assets",
                idx,
            )
        )

    return issues


def validate_negative_profit(df: pd.DataFrame):
    issues = []

    if "net_profit" not in df.columns:
        return issues

    invalid = df[df["net_profit"] < 0]

    for idx in invalid.index:
        issues.append(
            _build_issue(
                "DQ-06",
                "MEDIUM",
                "net_profit",
                "Negative profit",
                idx,
            )
        )

    return issues


def validate_missing_year(df: pd.DataFrame):
    issues = []

    if "year" not in df.columns:
        return issues

    invalid = df[df["year"].isna()]

    for idx in invalid.index:
        issues.append(
            _build_issue(
                "DQ-07",
                "HIGH",
                "year",
                "Missing year",
                idx,
            )
        )

    return issues


def validate_duplicate_year(df: pd.DataFrame):
    issues = []

    if {"company_id", "year"}.issubset(df.columns):
        dup = df[df.duplicated(["company_id", "year"], keep=False)]

        for idx in dup.index:
            issues.append(
                _build_issue(
                    "DQ-08",
                    "HIGH",
                    "year",
                    "Duplicate company/year",
                    idx,
                )
            )

    return issues


def validate_negative_cashflow(df: pd.DataFrame):
    issues = []

    if "cash_flow" not in df.columns:
        return issues

    invalid = df[df["cash_flow"] < 0]

    for idx in invalid.index:
        issues.append(
            _build_issue(
                "DQ-09",
                "LOW",
                "cash_flow",
                "Negative cash flow",
                idx,
            )
        )

    return issues


def validate_missing_sector(df: pd.DataFrame):
    issues = []

    if "sector" not in df.columns:
        return issues

    invalid = df[df["sector"].isna()]

    for idx in invalid.index:
        issues.append(
            _build_issue(
                "DQ-10",
                "MEDIUM",
                "sector",
                "Missing sector",
                idx,
            )
        )

    return issues


def validate_missing_company_name(df: pd.DataFrame):
    issues = []

    if "company_name" not in df.columns:
        return issues

    invalid = df[df["company_name"].isna()]

    for idx in invalid.index:
        issues.append(
            _build_issue(
                "DQ-11",
                "HIGH",
                "company_name",
                "Missing company name",
                idx,
            )
        )

    return issues


def validate_negative_equity(df: pd.DataFrame):
    issues = []

    if "equity" not in df.columns:
        return issues

    invalid = df[df["equity"] < 0]

    for idx in invalid.index:
        issues.append(
            _build_issue(
                "DQ-12",
                "MEDIUM",
                "equity",
                "Negative equity",
                idx,
            )
        )

    return issues


def validate_missing_market_cap(df: pd.DataFrame):
    issues = []

    if "market_cap" not in df.columns:
        return issues

    invalid = df[df["market_cap"].isna()]

    for idx in invalid.index:
        issues.append(
            _build_issue(
                "DQ-13",
                "MEDIUM",
                "market_cap",
                "Missing market cap",
                idx,
            )
        )

    return issues


def validate_duplicate_ticker(df: pd.DataFrame):
    issues = []

    if "ticker" not in df.columns:
        return issues

    dup = df[df.duplicated("ticker", keep=False)]

    for idx in dup.index:
        issues.append(
            _build_issue(
                "DQ-14",
                "HIGH",
                "ticker",
                "Duplicate ticker",
                idx,
            )
        )

    return issues