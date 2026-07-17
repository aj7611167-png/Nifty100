import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_market_cap,
    get_dashboard_data
)

# =====================================================
# PAGE TITLE
# =====================================================

st.title("💰 Capital Analysis")

st.markdown(
    "Analyze Market Capitalization, Enterprise Value and Valuation Ratios."
)

# =====================================================
# LOAD DATA
# =====================================================

market_df = get_market_cap()
dashboard_df = get_dashboard_data()

if market_df.empty:
    st.warning("Market Cap data not available.")
    st.stop()

# =====================================================
# MERGE DATA
# =====================================================

df = market_df.merge(
    dashboard_df[
        [
            "id",
            "company_name",
            "broad_sector",
            "sub_sector"
        ]
    ].drop_duplicates(),
    left_on="company_id",
    right_on="id",
    how="left"
)

# =====================================================
# LATEST YEAR DATA
# =====================================================

latest = (
    df
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)

st.markdown("---")
st.subheader("📊 Valuation Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average P/E",
        f"{latest['pe_ratio'].mean():.2f}"
    )

with col2:
    st.metric(
        "Average P/B",
        f"{latest['pb_ratio'].mean():.2f}"
    )

with col3:
    st.metric(
        "Average EV/EBITDA",
        f"{latest['ev_ebitda'].mean():.2f}"
    )

with col4:
    st.metric(
        "Average Dividend Yield",
        f"{latest['dividend_yield_pct'].mean():.2f}%"
    )

# =====================================================
# TOP MARKET CAP COMPANIES
# =====================================================

st.markdown("---")
st.subheader("🏆 Top 15 Companies by Market Capitalization")

top_market_cap = (
    latest
    .sort_values(
        "market_cap_crore",
        ascending=False
    )
    .head(15)
)

fig = px.bar(
    top_market_cap,
    x="company_name",
    y="market_cap_crore",
    color="broad_sector",
    title="Top 15 Companies by Market Capitalization"
)

fig.update_layout(
    xaxis_title="Company",
    yaxis_title="Market Cap (₹ Crore)",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# MARKET CAP DISTRIBUTION
# =====================================================

st.markdown("---")
st.subheader("📊 Market Cap Distribution")

fig = px.histogram(
    latest,
    x="market_cap_crore",
    nbins=20,
    title="Distribution of Market Capitalization"
)

fig.update_layout(
    xaxis_title="Market Capitalization (₹ Crore)",
    yaxis_title="Number of Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# P/E vs P/B ANALYSIS
# =====================================================

st.markdown("---")
st.subheader("📈 P/E Ratio vs P/B Ratio")

scatter_df = latest.dropna(
    subset=[
        "pe_ratio",
        "pb_ratio",
        "market_cap_crore"
    ]
)

fig = px.scatter(
    scatter_df,
    x="pe_ratio",
    y="pb_ratio",
    size="market_cap_crore",
    color="broad_sector",
    hover_name="company_name",
    title="P/E Ratio vs P/B Ratio"
)

fig.update_layout(
    xaxis_title="P/E Ratio",
    yaxis_title="P/B Ratio"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TOP DIVIDEND YIELD COMPANIES
# =====================================================

st.markdown("---")
st.subheader("💰 Top 15 Dividend Yield Companies")

dividend_df = (
    latest
    .dropna(subset=["dividend_yield_pct"])
    .sort_values(
        "dividend_yield_pct",
        ascending=False
    )
    .head(15)
)

fig = px.bar(
    dividend_df,
    x="company_name",
    y="dividend_yield_pct",
    color="broad_sector",
    title="Top 15 Dividend Yield Companies"
)

fig.update_layout(
    xaxis_title="Company",
    yaxis_title="Dividend Yield (%)",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TOP VALUE STOCKS
# =====================================================

st.markdown("---")
st.subheader("⭐ Top Value Stocks")

value_df = (
    latest[
        [
            "company_name",
            "broad_sector",
            "market_cap_crore",
            "pe_ratio",
            "pb_ratio",
            "dividend_yield_pct"
        ]
    ]
    .dropna(subset=["pe_ratio", "pb_ratio"])
)

value_df = (
    value_df[
        (value_df["pe_ratio"] > 0) &
        (value_df["pb_ratio"] > 0)
    ]
    .sort_values(
        ["pe_ratio", "pb_ratio"]
    )
    .head(15)
)

st.dataframe(
    value_df,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# DOWNLOAD DATA
# =====================================================

st.markdown("---")

csv = latest.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Capital Analysis Data",
    data=csv,
    file_name="capital_analysis.csv",
    mime="text/csv"
)

# =====================================================
# OVERVIEW TABLE
# =====================================================

st.markdown("---")

st.subheader("📋 Company Valuation Overview")

st.dataframe(
    latest[
        [
            "company_name",
            "broad_sector",
            "market_cap_crore",
            "enterprise_value_crore",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "dividend_yield_pct"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# =====================================================
# CAPITAL INSIGHTS
# =====================================================

st.markdown("---")
st.subheader("💡 Capital Market Insights")

largest = latest.loc[
    latest["market_cap_crore"].idxmax()
]

highest_dividend = latest.loc[
    latest["dividend_yield_pct"].idxmax()
]

lowest_pe = (
    latest[latest["pe_ratio"] > 0]
    .sort_values("pe_ratio")
    .iloc[0]
)

col1, col2, col3 = st.columns(3)

with col1:
    st.success(
        f"""
### 🏆 Largest Company

**{largest['company_name']}**

Market Cap

₹ {largest['market_cap_crore']:,.0f} Cr
"""
    )

with col2:
    st.info(
        f"""
### 💰 Highest Dividend

**{highest_dividend['company_name']}**

Dividend Yield

{highest_dividend['dividend_yield_pct']:.2f}%
"""
    )

with col3:
    st.warning(
        f"""
### 📉 Lowest P/E

**{lowest_pe['company_name']}**

P/E Ratio

{lowest_pe['pe_ratio']:.2f}
"""
    )