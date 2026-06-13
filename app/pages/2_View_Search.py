"""
2_View_Search.py  –  View, search, and filter opportunities
"""
import streamlit as st
import pandas as pd
from app.queries import search_opportunities, get_all_opportunities
from app.utils import (
    CATEGORIES, WORK_MODES, STATUSES, EXPERIENCE_LEVELS,
    df_to_csv_bytes, display_no_data_message, format_salary, status_badge
)

st.title("🔍 View & Search Opportunities")

# ── Sidebar filters ───────────────────────────────────────────
with st.sidebar:
    st.header("🔎 Filters")
    keyword          = st.text_input("Keyword (company, title, skills)")
    sel_category     = st.selectbox("Category",         ["All"] + CATEGORIES)
    sel_city         = st.text_input("City")
    sel_work_mode    = st.selectbox("Work Mode",        ["All"] + WORK_MODES)
    sel_status       = st.selectbox("Status",           ["All"] + STATUSES)
    sel_experience   = st.selectbox("Experience Level", ["All"] + EXPERIENCE_LEVELS)
    salary_range     = st.slider("Salary Range (PKR)", 0, 600_000, (0, 600_000), step=5000)
    apply_filters    = st.button("Apply Filters", use_container_width=True)
    clear_filters    = st.button("Clear Filters",  use_container_width=True)

if clear_filters:
    st.rerun()

# ── Fetch data ────────────────────────────────────────────────
try:
    df = search_opportunities(
        keyword        = keyword,
        category       = "" if sel_category  == "All" else sel_category,
        city           = sel_city,
        work_mode      = "" if sel_work_mode  == "All" else sel_work_mode,
        status         = "" if sel_status     == "All" else sel_status,
        experience_level = "" if sel_experience == "All" else sel_experience,
        salary_min     = salary_range[0],
        salary_max     = salary_range[1],
    )
except Exception as e:
    st.error(f"❌ Could not load data: {e}")
    st.stop()

# ── Summary metrics ───────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Records",    len(df))
m2.metric("Open",             len(df[df["status"] == "Open"]) if not df.empty else 0)
m3.metric("Shortlisted",      len(df[df["status"] == "Shortlisted"]) if not df.empty else 0)
m4.metric("Companies",        df["company_name"].nunique() if not df.empty else 0)

st.divider()

if df.empty:
    display_no_data_message("your search criteria")
else:
    # ── Display table ─────────────────────────────────────────
    display_cols = [
        "opportunity_id", "company_name", "job_title", "category",
        "city", "work_mode", "experience_level",
        "salary_min", "salary_max", "currency",
        "status", "application_deadline",
    ]
    existing_cols = [c for c in display_cols if c in df.columns]
    st.dataframe(df[existing_cols], use_container_width=True, hide_index=True)

    # ── Export filtered results ───────────────────────────────
    st.download_button(
        label="📥 Export Filtered Results as CSV",
        data=df_to_csv_bytes(df),
        file_name="opportunities_filtered.csv",
        mime="text/csv",
        use_container_width=True,
    )

    # ── Detail expander ───────────────────────────────────────
    st.subheader("🔎 Record Detail")
    ids = df["opportunity_id"].tolist()
    sel_id = st.selectbox("Select Opportunity ID to view full details", ids)
    if sel_id:
        row = df[df["opportunity_id"] == sel_id].iloc[0]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Company:** {row['company_name']}")
            st.markdown(f"**Title:** {row['job_title']}")
            st.markdown(f"**Category:** {row['category']}")
            st.markdown(f"**Location:** {row.get('city', '')} — {row.get('country', '')}")
            st.markdown(f"**Work Mode:** {row['work_mode']}")
            st.markdown(f"**Experience:** {row.get('experience_level', 'N/A')}")
        with c2:
            st.markdown(f"**Status:** {status_badge(row['status'])}")
            st.markdown(f"**Salary:** {format_salary(row.get('salary_min'), row.get('salary_max'), row.get('currency', 'PKR'))}")
            st.markdown(f"**Deadline:** {row.get('application_deadline', 'N/A')}")
            st.markdown(f"**Skills:** {row.get('required_skills', 'N/A')}")
            if row.get('source_link'):
                st.markdown(f"**Link:** [{row['source_link']}]({row['source_link']})")
