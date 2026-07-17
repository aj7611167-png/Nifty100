import streamlit as st
import pandas as pd

from utils.db import get_dashboard_data

# =====================================================
# PAGE TITLE
# =====================================================

st.title("🔎 Stock Screener")

st.write(
    "Filter Nifty 100 companies using financial metrics."
)

# =====================================================
# LOAD DATA
# =====================================================

df = get_dashboard_data()

# =====================================================
# FILTERS
# =====================================================

st.sidebar.header("Filters")

# -------------------------
# Sector
# -------------------------

sectors = sorted(df["broad_sector"].dropna().unique())

selected_sector = st.sidebar.selectbox(
    "Sector",
    ["All"] + sectors
)

# -------------------------
# ROE
# -------------------------

min_roe = st.sidebar.slider(
    "Minimum ROE (%)",
    min_value=0.0,
    max_value=50.0,
    value=10.0,
    step=1.0
)

# -------------------------
# ROCE
# -------------------------

min_roce = st.sidebar.slider(
    "Minimum ROCE (%)",
    min_value=0.0,
    max_value=60.0,
    value=10.0,
    step=1.0
)

# -------------------------
# Debt to Equity
# -------------------------

max_debt = st.sidebar.slider(
    "Maximum Debt/Equity",
    min_value=0.0,
    max_value=5.0,
    value=2.0,
    step=0.1
)

# -------------------------
# Quality Score
# -------------------------

min_quality = st.sidebar.slider(
    "Minimum Quality Score",
    min_value=0,
    max_value=100,
    value=50,
    step=5
)

# -------------------------
# Revenue CAGR
# -------------------------

min_cagr = st.sidebar.slider(
    "Minimum Revenue CAGR (5Y)",
    min_value=-20.0,
    max_value=50.0,
    value=0.0,
    step=1.0
)

# -------------------------
# Free Cash Flow
# -------------------------

min_fcf = st.sidebar.number_input(
    "Minimum Free Cash Flow (Cr)",
    value=0.0,
    step=100.0
)

# =====================================================
# APPLY FILTERS
# =====================================================

filtered_df = df.copy()

if selected_sector != "All":
    filtered_df = filtered_df[
        filtered_df["broad_sector"] == selected_sector
    ]

filtered_df = filtered_df[
    filtered_df["return_on_equity_pct"] >= min_roe
]

filtered_df = filtered_df[
    filtered_df["roce_percentage"] >= min_roce
]

filtered_df = filtered_df[
    filtered_df["debt_to_equity"] <= max_debt
]

filtered_df = filtered_df[
    filtered_df["composite_quality_score"] >= min_quality
]

filtered_df = filtered_df[
    filtered_df["revenue_cagr_5yr"] >= min_cagr
]

filtered_df = filtered_df[
    filtered_df["free_cash_flow_cr"] >= min_fcf
]

# =====================================================
# RESULTS
# =====================================================

st.markdown("---")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Companies",
    len(filtered_df)
)

c2.metric(
    "Average ROE",
    f"{filtered_df['return_on_equity_pct'].mean():.2f}%"
)

c3.metric(
    "Average ROCE",
    f"{filtered_df['roce_percentage'].mean():.2f}%"
)

c4.metric(
    "Average Quality",
    f"{filtered_df['composite_quality_score'].mean():.1f}"
)

st.subheader("📊 Filtered Companies")

display_df = filtered_df[
    [
        "company_name",
        "broad_sector",
        "return_on_equity_pct",
        "roce_percentage",
        "debt_to_equity",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "composite_quality_score"
    ]
].copy()

display_df = display_df.rename(
    columns={
        "company_name": "Company",
        "broad_sector": "Sector",
        "return_on_equity_pct": "ROE (%)",
        "roce_percentage": "ROCE (%)",
        "debt_to_equity": "Debt/Equity",
        "free_cash_flow_cr": "Free Cash Flow (Cr)",
        "revenue_cagr_5yr": "Revenue CAGR 5Y (%)",
        "composite_quality_score": "Quality Score"
    }
)

display_df = display_df.sort_values(
    "Quality Score",
    ascending=False
)

st.write(f"### Total Companies Found: {len(display_df)}")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Results as CSV",
    data=csv,
    file_name="nifty100_screener.csv",
    mime="text/csv"
)

