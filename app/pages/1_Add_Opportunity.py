"""
1_Add_Opportunity.py  –  Add a new internship/job opportunity (Admin only)
"""
import streamlit as st
from app.auth import require_admin
from app.queries import insert_opportunity, find_duplicates
from app.utils import CATEGORIES, WORK_MODES, STATUSES, EXPERIENCE_LEVELS, CURRENCIES

require_admin()

st.title("➕ Add New Opportunity")
st.markdown("Fill in the form below to add a new internship or job opportunity to the database.")

with st.form("add_opportunity_form", clear_on_submit=True):
    st.subheader("Company & Role")
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("Company Name *", max_chars=100)
        job_title    = st.text_input("Job Title *", max_chars=150)
        category     = st.selectbox("Category *", CATEGORIES)
    with col2:
        city             = st.text_input("City", max_chars=80)
        country          = st.text_input("Country", value="Pakistan", max_chars=80)
        experience_level = st.selectbox("Experience Level", [""] + EXPERIENCE_LEVELS)

    st.subheader("Work & Salary")
    col3, col4, col5 = st.columns(3)
    with col3:
        work_mode = st.selectbox("Work Mode *", WORK_MODES)
        status    = st.selectbox("Status *", STATUSES)
    with col4:
        salary_min = st.number_input("Salary Min", min_value=0.0, step=1000.0, value=0.0)
        salary_max = st.number_input("Salary Max", min_value=0.0, step=1000.0, value=0.0)
    with col5:
        currency             = st.selectbox("Currency", CURRENCIES)
        application_deadline = st.date_input("Application Deadline", value=None)

    st.subheader("Details")
    required_skills = st.text_area("Required Skills * (comma-separated)", max_chars=500)
    source_link     = st.text_input("Source / Job Link", max_chars=500)

    submitted = st.form_submit_button("💾 Save Opportunity", use_container_width=True)

if submitted:
    # ── Validation ────────────────────────────────────────────
    errors = []
    if not company_name.strip():
        errors.append("Company Name is required.")
    if not job_title.strip():
        errors.append("Job Title is required.")
    if not required_skills.strip():
        errors.append("Required Skills is required.")
    if salary_max and salary_min and salary_max < salary_min:
        errors.append("Salary Max must be >= Salary Min.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        data = {
            "company_name":         company_name.strip(),
            "job_title":            job_title.strip(),
            "category":             category,
            "city":                 city.strip() or None,
            "country":              country.strip() or None,
            "work_mode":            work_mode,
            "required_skills":      required_skills.strip(),
            "salary_min":           salary_min if salary_min > 0 else None,
            "salary_max":           salary_max if salary_max > 0 else None,
            "currency":             currency,
            "experience_level":     experience_level or None,
            "application_deadline": application_deadline,
            "status":               status,
            "source_link":          source_link.strip() or None,
        }
        try:
            new_id = insert_opportunity(data)
            st.success(f"✅ Opportunity added successfully! ID: **{new_id}**")
            st.balloons()
        except Exception as e:
            st.error(f"❌ Database error: {e}")
