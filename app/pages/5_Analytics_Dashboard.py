"""
5_Analytics_Dashboard.py  –  Analytics dashboard with 6 KPIs and 5+ Plotly charts
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from app.queries import (
    get_kpi_summary, get_category_counts, get_work_mode_counts,
    get_status_counts, get_city_counts, get_company_counts,
    get_salary_by_category, get_skills_frequency,
)

st.title("📊 Analytics Dashboard")
st.markdown("Real-time insights from the PostgreSQL opportunities database.")

# ── KPIs ──────────────────────────────────────────────────────
try:
    kpi = get_kpi_summary()
except Exception as e:
    st.error(f"❌ Could not load KPIs: {e}")
    st.stop()

st.subheader("📈 Key Performance Indicators")
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Opportunities", kpi.get("total", 0))
k2.metric("Open",                kpi.get("open_count", 0))
k3.metric("Closed",              kpi.get("closed_count", 0))
k4.metric("Expired",             kpi.get("expired_count", 0))
k5.metric("Companies",           kpi.get("companies", 0))
k6.metric("Avg Salary (PKR)",    f"{int(kpi.get('avg_salary') or 0):,}")

st.divider()

# ── Charts ────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📂 Category", "🌐 Work Mode", "🏙️ City", "💰 Salary", "🔧 Skills"
])

# Chart 1 – Opportunities by Category
with tab1:
    try:
        cat_df = get_category_counts()
        if not cat_df.empty:
            fig = px.bar(
                cat_df, x="category", y="count",
                title="Opportunities by Category",
                color="count", color_continuous_scale="Blues",
                labels={"count": "Count", "category": "Category"},
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

            # Pie chart alongside
            fig2 = px.pie(
                cat_df, names="category", values="count",
                title="Category Distribution",
                hole=0.4,
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No data available.")
    except Exception as e:
        st.error(str(e))

# Chart 2 – Work Mode distribution
with tab2:
    try:
        wm_df = get_work_mode_counts()
        status_df = get_status_counts()

        col1, col2 = st.columns(2)
        with col1:
            if not wm_df.empty:
                fig = px.pie(
                    wm_df, names="work_mode", values="count",
                    title="Work Mode Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set2,
                    hole=0.3,
                )
                st.plotly_chart(fig, use_container_width=True)
        with col2:
            if not status_df.empty:
                fig2 = px.bar(
                    status_df, x="status", y="count",
                    title="Opportunities by Status",
                    color="status",
                    color_discrete_map={
                        "Open": "#2ECC71", "Closed": "#E74C3C",
                        "Expired": "#F39C12", "Shortlisted": "#3498DB",
                    },
                )
                fig2.update_layout(showlegend=False)
                st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(str(e))

# Chart 3 – Top Cities + Company breakdown
with tab3:
    try:
        city_df    = get_city_counts()
        company_df = get_company_counts()

        col1, col2 = st.columns(2)
        with col1:
            if not city_df.empty:
                fig = px.bar(
                    city_df.head(10), x="count", y="city",
                    orientation="h",
                    title="Top Cities by Opportunity Count",
                    color="count", color_continuous_scale="Teal",
                )
                fig.update_layout(yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig, use_container_width=True)
        with col2:
            if not company_df.empty:
                fig2 = px.bar(
                    company_df, x="company_name", y="count",
                    title="Opportunities per Company",
                    color="count", color_continuous_scale="Purples",
                )
                fig2.update_layout(xaxis_tickangle=-30)
                st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(str(e))

# Chart 4 – Salary analysis
with tab4:
    try:
        sal_df = get_salary_by_category()
        if not sal_df.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name="Avg Min Salary",
                x=sal_df["category"], y=sal_df["avg_min"],
                marker_color="#85C1E9",
            ))
            fig.add_trace(go.Bar(
                name="Avg Max Salary",
                x=sal_df["category"], y=sal_df["avg_max"],
                marker_color="#2471A3",
            ))
            fig.update_layout(
                title="Average Salary Range by Category (PKR)",
                barmode="group",
                yaxis_title="Salary (PKR)",
                xaxis_title="Category",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No salary data available.")
    except Exception as e:
        st.error(str(e))

# Chart 5 – Top Skills
with tab5:
    try:
        skills_df = get_skills_frequency()
        if not skills_df.empty:
            fig = px.bar(
                skills_df, x="count", y="skill",
                orientation="h",
                title="Top 20 Most Required Skills",
                color="count", color_continuous_scale="Oranges",
            )
            fig.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No skills data available.")
    except Exception as e:
        st.error(str(e))
