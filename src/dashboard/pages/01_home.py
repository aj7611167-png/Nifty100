import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import plotly.express as px

from utils.db import get_dashboard_data

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD DATA
# =====================================================

df = get_dashboard_data()

# =====================================================
# TITLE
# =====================================================

st.title("📊 Nifty 100 Analytics Dashboard")

# =====================================================
# YEAR FILTER
# =====================================================

years = sorted(df["year"].dropna().unique())

selected_year = st.sidebar.selectbox(
    "Financial Year",
    years,
    index=len(years) - 1
)

df = df[df["year"] == selected_year]

# =====================================================
# KPI CALCULATIONS
# =====================================================

avg_roe = round(df["return_on_equity_pct"].mean(), 2)
median_de = round(df["debt_to_equity"].median(), 2)
median_cagr = round(df["revenue_cagr_5yr"].median(), 2)
companies = df["id"].nunique()
debt_free = len(df[df["debt_to_equity"] <= 0])

# =====================================================
# KPI CARDS
# =====================================================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Average ROE", f"{avg_roe}%")
c2.metric("Median D/E", median_de)
c3.metric("Companies", companies)
c4.metric("Median Revenue CAGR", f"{median_cagr}%")
c5.metric("Debt Free", debt_free)


# =====================================================
# SECTOR BREAKDOWN
# =====================================================

st.markdown("---")
st.subheader("Sector Breakdown")

sector_df = (
    df.groupby("broad_sector")["id"]
      .nunique()
      .reset_index(name="Companies")
)

fig = px.pie(
    sector_df,
    names="broad_sector",
    values="Companies",
    hole=0.5,
    title="Companies by Sector"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# =====================================================
# TOP 5 COMPANIES BY QUALITY SCORE
# =====================================================

st.markdown("---")
st.subheader("🏆 Top 5 Companies by Composite Quality Score")

top5 = (
    df.sort_values(
        "composite_quality_score",
        ascending=False
    )[[
        "id",
        "company_name",
        "broad_sector",
        "composite_quality_score",
        "return_on_equity_pct"
    ]]
    .head(5)
)

st.dataframe(
    top5,
    width="stretch"
)