import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_dashboard_data,
    get_pl,
    get_cf
)

# =====================================================
# PAGE TITLE
# =====================================================

st.title("📈 Financial Trends")
st.markdown("Analyze historical financial trends for any company.")

# =====================================================
# LOAD DATA
# =====================================================

df = get_dashboard_data()

companies = sorted(df["company_name"].unique())

company = st.selectbox(
    "Select Company",
    companies
)

selected = df[df["company_name"] == company]

if selected.empty:
    st.warning("Company not found.")
    st.stop()

latest = (
    selected
    .sort_values("year", ascending=False)
    .iloc[0]
)

# =====================================================
# LOAD DATA
# =====================================================

pl = get_pl(latest["id"])
cf = get_cf(latest["id"])

# =====================================================
# SALES & NET PROFIT TREND
# =====================================================

st.markdown("---")
st.subheader("📊 Sales & Net Profit Trend")

if not pl.empty:

    pl = pl.sort_values("year")

    fig = px.line(
        pl,
        x="year",
        y=["sales", "net_profit"],
        markers=True,
        title="Sales vs Net Profit"
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="₹ Crore"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.info("Profit & Loss data not available.")

# =====================================================
# ROE vs ROCE TREND
# =====================================================

st.markdown("---")
st.subheader("📈 ROE vs ROCE Trend")

chart_df = selected.sort_values("year")

fig = px.line(
    chart_df,
    x="year",
    y=[
        "return_on_equity_pct",
        "roce_percentage"
    ],
    markers=True,
    title="ROE vs ROCE"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Percentage (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# REVENUE CAGR DISTRIBUTION
# =====================================================

st.markdown("---")
st.subheader("📊 Revenue CAGR Distribution")

hist_df = df.dropna(subset=["revenue_cagr_5yr"])

fig = px.histogram(
    hist_df,
    x="revenue_cagr_5yr",
    nbins=20,
    title="5-Year Revenue CAGR Distribution"
)

fig.update_layout(
    xaxis_title="Revenue CAGR (%)",
    yaxis_title="Number of Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# NET CASH FLOW TREND
# =====================================================

st.markdown("---")
st.subheader("💰 Net Cash Flow Trend")

if not cf.empty:

    cf = cf.sort_values("year")

    fig = px.bar(
        cf,
        x="year",
        y="net_cash_flow",
        text="net_cash_flow",
        title="Net Cash Flow by Year"
    )

    fig.update_traces(
        texttemplate="%{text:.0f}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="₹ Crore"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.info("Cash Flow data not available.")

# =====================================================
# FINANCIAL SUMMARY
# =====================================================

st.markdown("---")
st.subheader("📋 Financial Summary")

c1, c2, c3, c4 = st.columns(4)

roe = latest["return_on_equity_pct"]
roce = latest["roce_percentage"]
cagr = latest["revenue_cagr_5yr"]
fcf = latest["free_cash_flow_cr"]

with c1:
    st.metric(
        "ROE",
        "N/A" if pd.isna(roe) else f"{roe:.2f}%"
    )

with c2:
    st.metric(
        "ROCE",
        "N/A" if pd.isna(roce) else f"{roce:.2f}%"
    )

with c3:
    st.metric(
        "Revenue CAGR",
        "N/A" if pd.isna(cagr) else f"{cagr:.2f}%"
    )

with c4:
    st.metric(
        "Free Cash Flow",
        "N/A" if pd.isna(fcf) else f"₹ {fcf:.2f} Cr"
    )

# =====================================================
# DOWNLOAD DATA
# =====================================================

st.markdown("---")

csv = (
    selected
    .sort_values("year")
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    label="📥 Download Trend Data",
    data=csv,
    file_name=f"{latest['company_name']}_trend_data.csv",
    mime="text/csv"
)

# =====================================================
# TREND INSIGHTS
# =====================================================

st.markdown("---")
st.subheader("🧠 Trend Insights")

insights = []

if not pd.isna(roe):
    if roe >= 20:
        insights.append(
            f"✅ Strong ROE of **{roe:.2f}%** indicates efficient use of shareholders' equity."
        )
    elif roe >= 15:
        insights.append(
            f"🟡 ROE of **{roe:.2f}%** is healthy."
        )
    else:
        insights.append(
            f"⚠️ ROE of **{roe:.2f}%** is relatively low."
        )

if not pd.isna(roce):
    if roce >= 20:
        insights.append(
            f"✅ ROCE of **{roce:.2f}%** suggests efficient capital utilization."
        )
    else:
        insights.append(
            f"⚠️ ROCE of **{roce:.2f}%** could be improved."
        )

if not pd.isna(cagr):
    if cagr >= 15:
        insights.append(
            f"📈 Revenue CAGR of **{cagr:.2f}%** reflects strong long-term growth."
        )
    elif cagr >= 5:
        insights.append(
            f"📊 Revenue CAGR of **{cagr:.2f}%** indicates moderate growth."
        )
    else:
        insights.append(
            f"📉 Revenue CAGR of **{cagr:.2f}%** is relatively low."
        )

if not pd.isna(fcf):
    if fcf > 0:
        insights.append(
            "💰 The company is generating positive free cash flow."
        )
    else:
        insights.append(
            "⚠️ The company has negative free cash flow."
        )

if insights:
    for item in insights:
        st.write(item)
else:
    st.info("No insights available.")