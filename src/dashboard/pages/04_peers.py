import streamlit as st
import plotly.express as px

from utils.db import get_dashboard_data

# =====================================================
# PAGE TITLE
# =====================================================

st.title("🤝 Peer Comparison")

# =====================================================
# LOAD DATA
# =====================================================

df = get_dashboard_data()

# =====================================================
# COMPANY SELECTION
# =====================================================

companies = sorted(df["company_name"].unique())

selected_companies = st.multiselect(
    "Select Companies",
    companies,
    default=companies[:3]
)

if len(selected_companies) < 2:
    st.warning("Please select at least 2 companies.")
    st.stop()

comparison_df = (
    df[df["company_name"].isin(selected_companies)]
    .sort_values("year")
)

latest = (
    comparison_df
    .sort_values("year")
    .groupby("company_name")
    .tail(1)
)

st.subheader("Latest Financial Comparison")

st.dataframe(
    latest[
        [
            "company_name",
            "broad_sector",
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
# ROE COMPARISON
# =====================================================

st.markdown("---")
st.subheader("📈 Return on Equity (ROE) Comparison")

fig = px.bar(
    latest,
    x="company_name",
    y="return_on_equity_pct",
    color="company_name",
    text="return_on_equity_pct",
    title="Latest ROE (%)"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Company",
    yaxis_title="ROE (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# ROCE COMPARISON
# =====================================================

st.markdown("---")
st.subheader("🏭 ROCE Comparison")

fig = px.bar(
    latest,
    x="company_name",
    y="roce_percentage",
    color="company_name",
    text="roce_percentage",
    title="Latest ROCE (%)"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Company",
    yaxis_title="ROCE (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# QUALITY SCORE
# =====================================================

st.markdown("---")
st.subheader("⭐ Quality Score Comparison")

fig = px.bar(
    latest,
    x="company_name",
    y="composite_quality_score",
    color="company_name",
    text="composite_quality_score",
    title="Quality Score"
)

fig.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Company",
    yaxis_title="Quality Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# REVENUE CAGR
# =====================================================

st.markdown("---")
st.subheader("📊 Revenue CAGR (5Y)")

fig = px.bar(
    latest,
    x="company_name",
    y="revenue_cagr_5yr",
    color="company_name",
    text="revenue_cagr_5yr",
    title="Revenue CAGR (5Y)"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Company",
    yaxis_title="Revenue CAGR (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# FREE CASH FLOW
# =====================================================

st.markdown("---")
st.subheader("💰 Free Cash Flow")

fig = px.bar(
    latest,
    x="company_name",
    y="free_cash_flow_cr",
    color="company_name",
    text="free_cash_flow_cr",
    title="Free Cash Flow"
)

fig.update_traces(
    texttemplate="%{text:.0f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Company",
    yaxis_title="₹ Crore"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TOP PERFORMERS
# =====================================================

st.markdown("---")
st.subheader("🏆 Top Performers")

c1, c2, c3 = st.columns(3)

roe_winner = latest.loc[latest["return_on_equity_pct"].idxmax()]
roce_winner = latest.loc[latest["roce_percentage"].idxmax()]
quality_winner = latest.loc[latest["composite_quality_score"].idxmax()]

with c1:
    st.success("Highest ROE")
    st.metric(
        roe_winner["company_name"],
        f"{roe_winner['return_on_equity_pct']:.2f}%"
    )

with c2:
    st.success("Highest ROCE")
    st.metric(
        roce_winner["company_name"],
        f"{roce_winner['roce_percentage']:.2f}%"
    )

with c3:
    st.success("Best Quality Score")
    st.metric(
        quality_winner["company_name"],
        f"{quality_winner['composite_quality_score']:.1f}"
    )

# =====================================================
# DOWNLOAD COMPARISON
# =====================================================

st.markdown("---")

csv = latest.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Peer Comparison CSV",
    data=csv,
    file_name="peer_comparison.csv",
    mime="text/csv"
)

# =====================================================
# SUMMARY INSIGHTS
# =====================================================

st.markdown("---")
st.subheader("📋 Summary Insights")

best_roe = latest.loc[latest["return_on_equity_pct"].idxmax()]
best_roce = latest.loc[latest["roce_percentage"].idxmax()]
best_quality = latest.loc[latest["composite_quality_score"].idxmax()]
lowest_debt = latest.loc[latest["debt_to_equity"].idxmin()]

st.info(
    f"""
### Key Highlights

✅ Highest ROE: **{best_roe['company_name']}**
({best_roe['return_on_equity_pct']:.2f}%)

✅ Highest ROCE: **{best_roce['company_name']}**
({best_roce['roce_percentage']:.2f}%)

✅ Best Quality Score: **{best_quality['company_name']}**
({best_quality['composite_quality_score']:.1f})

✅ Lowest Debt/Equity: **{lowest_debt['company_name']}**
({lowest_debt['debt_to_equity']:.2f})
"""
)

