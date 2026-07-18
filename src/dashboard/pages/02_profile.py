import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_dashboard_data,
    get_pl,
    get_bs,
    get_cf,
    get_pros_cons
)

# =====================================================
# PAGE TITLE
# =====================================================

st.title("🏢 Company Profile")

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
# COMPANY INFORMATION
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
# LOAD PROFIT & LOSS DATA (ONLY ONCE)
# =====================================================

pl = get_pl(latest["id"])

net_profit_margin = None

if not pl.empty:

    latest_pl = (
        pl
        .sort_values("year", ascending=False)
        .iloc[0]
    )

    sales = latest_pl["sales"]
    net_profit = latest_pl["net_profit"]

    if (
        pd.notna(sales)
        and sales != 0
        and pd.notna(net_profit)
    ):
        net_profit_margin = (net_profit / sales) * 100

# =====================================================
# KEY FINANCIAL METRICS
# =====================================================

st.markdown("---")
st.subheader("Key Financial Metrics")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Net Profit Margin",
        "N/A"
        if net_profit_margin is None
        else f"{net_profit_margin:.2f}%"
    )

with c2:

    debt = latest["debt_to_equity"]

    st.metric(
        "Debt / Equity",
        "N/A"
        if pd.isna(debt)
        else f"{debt:.2f}"
    )

with c3:

    cagr = latest["revenue_cagr_5yr"]

    st.metric(
        "Revenue CAGR (5Y)",
        "N/A"
        if pd.isna(cagr)
        else f"{cagr:.2f}%"
    )

with c4:

    fcf = latest["free_cash_flow_cr"]

    st.metric(
        "Free Cash Flow",
        "N/A"
        if pd.isna(fcf)
        else f"₹ {fcf:.2f} Cr"
    )

# =====================================================
# SALES VS NET PROFIT
# =====================================================

st.markdown("---")
st.subheader("Sales vs Net Profit")

if not pl.empty:

    chart_pl = pl.sort_values("year")

    fig = px.bar(
        chart_pl,
        x="year",
        y=["sales", "net_profit"],
        barmode="group",
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
# ROE VS ROCE TREND
# =====================================================

st.markdown("---")
st.subheader("ROE vs ROCE Trend")

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
    yaxis_title="Percentage"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# BALANCE SHEET
# =====================================================

st.markdown("---")
st.subheader("Balance Sheet")

bs = get_bs(latest["id"])

if not bs.empty:

    bs = bs.sort_values("year")

    fig = px.line(
        bs,
        x="year",
        y=[
            "total_assets",
            "total_liabilities"
        ],
        markers=True,
        title="Assets vs Liabilities"
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

    st.info("Balance Sheet data not available.")

# =====================================================
# CASH FLOW
# =====================================================

st.markdown("---")
st.subheader("Net Cash Flow")

cf = get_cf(latest["id"])

if not cf.empty:

    cf = cf.sort_values("year")

    fig = px.bar(
        cf,
        x="year",
        y="net_cash_flow",
        title="Net Cash Flow"
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
# PROS & CONS
# =====================================================

st.markdown("---")
st.subheader("Pros & Cons")

pc = get_pros_cons(latest["id"])

if not pc.empty:

    row = pc.iloc[0]

    col1, col2 = st.columns(2)

    with col1:

        st.success("Pros")

        pros = str(row["pros"]).split(";")

        for p in pros:
            p = p.strip()

            if p:
                st.write(f"✅ {p}")

    with col2:

        st.error("Cons")

        cons = str(row["cons"]).split(";")

        for c in cons:
            c = c.strip()

            if c:
                st.write(f"❌ {c}")

else:

    st.info("Pros & Cons not available.")