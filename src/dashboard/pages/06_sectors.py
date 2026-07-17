import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_sectors,
    get_dashboard_data
)

# =====================================================
# PAGE TITLE
# =====================================================

st.title("🏭 Sector Analysis")

st.markdown(
    "Analyze Nifty 100 companies based on sector performance."
)

# =====================================================
# LOAD DATA
# =====================================================

sector_df = get_sectors()
dashboard_df = get_dashboard_data()

if sector_df.empty or dashboard_df.empty:
    st.warning("Sector data not available.")
    st.stop()

# =====================================================
# MERGE DATA
# =====================================================

df = dashboard_df.merge(
    sector_df[
        [
            "company_id",
            "index_weight_pct",
            "market_cap_category"
        ]
    ],
    left_on="id",
    right_on="company_id",
    how="left"
)

# =====================================================
# LATEST YEAR DATA
# =====================================================

latest = (
    df
    .sort_values("year", ascending=False)
    .drop_duplicates(subset="id")
    .copy()
)

# =====================================================
# COMPANY TABLE
# =====================================================

st.markdown("---")
st.subheader("📋 Sector Company Data")

company_table = latest[
    [
        "company_name",
        "broad_sector",
        "sub_sector",
        "return_on_equity_pct",
        "roce_percentage",
        "composite_quality_score",
        "market_cap_category",
        "index_weight_pct"
    ]
].sort_values(
    "composite_quality_score",
    ascending=False,
    na_position="last"
)

st.dataframe(
    company_table,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# SECTOR DISTRIBUTION
# =====================================================

st.markdown("---")
st.subheader("📊 Companies by Sector")

sector_count = (
    latest
    .groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
)

fig = px.pie(
    sector_count,
    names="broad_sector",
    values="Companies",
    title="Nifty 100 Sector Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# ROE & ROCE
# =====================================================

st.markdown("---")
st.subheader("📈 Average ROE & ROCE by Sector")

sector_perf = (
    latest
    .groupby("broad_sector", as_index=False)
    .agg({
        "return_on_equity_pct": "mean",
        "roce_percentage": "mean"
    })
)

fig = px.bar(
    sector_perf,
    x="broad_sector",
    y=[
        "return_on_equity_pct",
        "roce_percentage"
    ],
    barmode="group",
    title="Average ROE & ROCE"
)

fig.update_layout(
    xaxis_title="Sector",
    yaxis_title="Percentage",
    xaxis_tickangle=-30
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# ROE RANKING
# =====================================================

st.markdown("---")
st.subheader("📈 Average ROE by Sector")

roe_sector = (
    latest
    .groupby("broad_sector", as_index=False)
    .agg({
        "return_on_equity_pct": "mean"
    })
    .sort_values(
        "return_on_equity_pct",
        ascending=False
    )
)

fig = px.bar(
    roe_sector,
    x="broad_sector",
    y="return_on_equity_pct",
    title="Average ROE"
)

fig.update_layout(
    xaxis_tickangle=-30
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# QUALITY RANKING
# =====================================================

st.markdown("---")
st.subheader("🏆 Sector Quality Ranking")

quality = (
    latest
    .groupby("broad_sector", as_index=False)
    .agg({
        "composite_quality_score": "mean"
    })
    .sort_values(
        "composite_quality_score",
        ascending=False
    )
)

fig = px.bar(
    quality,
    x="broad_sector",
    y="composite_quality_score",
    title="Average Quality Score"
)

fig.update_layout(
    xaxis_tickangle=-30,
    yaxis_title="Quality Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# SECTOR FILTER
# =====================================================

st.markdown("---")
st.subheader("🏢 Companies by Sector")

sector_list = sorted(
    latest["broad_sector"]
    .dropna()
    .unique()
)

selected_sector = st.selectbox(
    "Select Sector",
    sector_list
)

sector_companies = (
    latest[
        latest["broad_sector"] == selected_sector
    ]
    .sort_values(
        "composite_quality_score",
        ascending=False,
        na_position="last"
    )
)

st.dataframe(
    sector_companies[
        [
            "company_name",
            "sub_sector",
            "return_on_equity_pct",
            "roce_percentage",
            "debt_to_equity",
            "free_cash_flow_cr",
            "composite_quality_score"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# =====================================================
# DOWNLOAD
# =====================================================

st.markdown("---")

csv = sector_companies.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Sector Data",
    csv,
    file_name=f"{selected_sector}_companies.csv",
    mime="text/csv"
)

# =====================================================
# INSIGHTS
# =====================================================

st.markdown("---")
st.subheader("💡 Sector Insights")

if sector_companies.empty:
    st.warning("No companies available.")
    st.stop()

best_company = sector_companies.iloc[0]

quality_score = (
    "N/A"
    if pd.isna(best_company["composite_quality_score"])
    else f"{best_company['composite_quality_score']:.1f}"
)

roe = (
    "N/A"
    if pd.isna(best_company["return_on_equity_pct"])
    else f"{best_company['return_on_equity_pct']:.2f}%"
)

roce = (
    "N/A"
    if pd.isna(best_company["roce_percentage"])
    else f"{best_company['roce_percentage']:.2f}%"
)

fcf = (
    "N/A"
    if pd.isna(best_company["free_cash_flow_cr"])
    else f"₹ {best_company['free_cash_flow_cr']:.2f} Cr"
)

st.success(
    f"""
### 🏆 Top Company in {selected_sector}

**{best_company['company_name']}**

⭐ Quality Score: {quality_score}

📈 ROE: {roe}

🏭 ROCE: {roce}

💰 Free Cash Flow: {fcf}
"""
)