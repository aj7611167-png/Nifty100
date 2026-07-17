import streamlit as st
import pandas as pd
from utils.db import (
    get_dashboard_data,
    get_pl,
    get_bs,
    get_cf
)
# =====================================================
# PAGE TITLE
# =====================================================
st.title("📄 Company Report Generator")
st.markdown(
    """
Generate a downloadable financial report
for any Nifty 100 company.
"""
)
# =====================================================
# LOAD DATA
# =====================================================
df = get_dashboard_data()
if df.empty:
    st.warning("No data available.")
    st.stop()
# =====================================================
# COMPANY SELECTOR
# =====================================================
companies = sorted(df["company_name"].unique())
company = st.selectbox(
    "Select Company",
    companies
)
selected = df[df["company_name"] == company]
latest = (
    selected
    .sort_values("year")
    .iloc[-1]
)
# =====================================================
# COMPANY SUMMARY
# =====================================================
st.markdown("---")
left, right = st.columns([2, 1])
with left:
    st.subheader(latest["company_name"])
    st.write(f"**Ticker:** {latest['id']}")
    st.write(f"**Sector:** {latest['broad_sector']}")
    st.write(f"**Sub Sector:** {latest['sub_sector']}")
with right:
    roe = latest["return_on_equity_pct"]
    roce = latest["roce_percentage"]
    st.metric(
        "ROE",
        "N/A" if pd.isna(roe) else f"{roe:.2f}%"
    )
    st.metric(
        "ROCE",
        "N/A" if pd.isna(roce) else f"{roce:.2f}%"
    )
# =====================================================
# LOAD FINANCIAL STATEMENTS
# =====================================================
pl = get_pl(latest["id"])
bs = get_bs(latest["id"])
cf = get_cf(latest["id"])
pl_latest = (
    pl.sort_values("year").iloc[-1]
    if not pl.empty
    else None
)
st.markdown("---")
# =====================================================
# PROFIT & LOSS
# =====================================================
st.subheader("📈 Profit & Loss Statement")
if not pl.empty:
    st.dataframe(
        pl.sort_values("year", ascending=False),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Profit & Loss data not available.")
# =====================================================
# BALANCE SHEET
# =====================================================
st.markdown("---")
st.subheader("🏦 Balance Sheet")
if not bs.empty:
    st.dataframe(
        bs.sort_values("year", ascending=False),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Balance Sheet data not available.")
# =====================================================
# CASH FLOW
# =====================================================
st.markdown("---")
st.subheader("💰 Cash Flow")
if not cf.empty:
    st.dataframe(
        cf.sort_values("year", ascending=False),
        use_container_width=True,
        hide_index=True
    )
else:

    st.info("Cash Flow data not available.")
# =====================================================
# FINANCIAL SUMMARY
# =====================================================
st.markdown("---")
st.subheader("📊 Financial Summary")
col1, col2, col3, col4 = st.columns(4)
# -----------------------------------------------------
with col1:
    if pl_latest is not None:

        value = pl_latest["opm_percentage"]
    else:

        value = None
    st.metric(
        "Operating Profit Margin",
        "N/A" if pd.isna(value) else f"{value:.2f}%"
    )
# -----------------------------------------------------
with col2:
    value = latest["debt_to_equity"]
    st.metric(
        "Debt / Equity",
        "N/A" if pd.isna(value) else f"{value:.2f}"
    )
# -----------------------------------------------------
with col3:

    value = latest["free_cash_flow_cr"]

    st.metric(
        "Free Cash Flow",
        "N/A" if pd.isna(value) else f"₹ {value:.2f} Cr"
    )
# -----------------------------------------------------
with col4:

    value = latest["composite_quality_score"]

    st.metric(
        "Quality Score",
        "N/A" if pd.isna(value) else f"{value:.1f}"
    )
# =====================================================
# GENERATE REPORT
# =====================================================

st.markdown("---")
st.subheader("📄 Download Company Report")

# Operating Profit Margin from Profit & Loss table
if pl_latest is not None:
    opm = pl_latest["opm_percentage"]
else:
    opm = None

report = pd.DataFrame({
    "Metric": [
        "Company",
        "Ticker",
        "Sector",
        "Sub Sector",
        "ROE",
        "ROCE",
        "Operating Profit Margin",
        "Debt / Equity",
        "Revenue CAGR (5Y)",
        "Free Cash Flow",
        "Quality Score"
    ],
    "Value": [
        latest["company_name"],
        latest["id"],
        latest["broad_sector"],
        latest["sub_sector"],
        latest["return_on_equity_pct"],
        latest["roce_percentage"],
        opm,
        latest["debt_to_equity"],
        latest["revenue_cagr_5yr"],
        latest["free_cash_flow_cr"],
        latest["composite_quality_score"]
    ]
})

st.dataframe(
    report,
    use_container_width=True,
    hide_index=True
)

csv = report.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Company Report (CSV)",
    data=csv,
    file_name=f"{latest['company_name']}_report.csv",
    mime="text/csv"
)
# =====================================================
# REPORT INSIGHTS
# =====================================================
st.markdown("---")
st.subheader("💡 Report Insights")
quality = latest["composite_quality_score"]
roe = latest["return_on_equity_pct"]
debt = latest["debt_to_equity"]
messages = []
if pd.notna(quality):
    if quality >= 80:
        messages.append("✅ Excellent overall quality score.")
    elif quality >= 60:
        messages.append("🟡 Good quality score.")
    else:
        messages.append("🔴 Below-average quality score.")
if pd.notna(roe):
    if roe >= 20:
        messages.append("📈 Strong Return on Equity.")
    elif roe >= 15:
        messages.append("📊 Healthy Return on Equity.")
    else:
        messages.append("⚠️ ROE is relatively low.")
if pd.notna(debt):
    if debt < 0.5:
        messages.append("💰 Low debt burden.")
    elif debt < 1:
        messages.append("🏦 Moderate debt level.")
    else:
        messages.append("⚠️ High debt-to-equity ratio.")
for msg in messages:
    st.success(msg)