import re
import pandas as pd


def normalize_year(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    match = re.search(r"(20\d{2})", value)

    if match:
        return int(match.group(1))

    return None


def normalize_ticker(value):
    if pd.isna(value):
        return None

    value = str(value).upper().strip()

    value = value.replace(".NS", "")
    value = value.replace(".BO", "")

    return value