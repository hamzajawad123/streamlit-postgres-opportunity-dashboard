"""
3_Update_Opportunity.py  –  Update an existing opportunity (Admin only)
"""
import streamlit as st
from app.auth import require_admin
from app.queries import get_all_opportunities, get_opportunity_by_id, update_opportunity
from app.utils import CATEGORIES, WORK_MODES, STATUSES, EXPERIENCE_LEVELS, CURRENCIES

require_admin()

st.title("✏️ Update Opportunity")

try:
    df = get_all_opportunities()
except Exception as e:
    st.error(f"❌ Could not load records: {e}")
    st.stop()

if df.empty:
    st.info("No opportunities found in the database.")
    st.stop()

# ── Select record ─────────────────────────────────────────────
st.subheader("1️⃣ Select a Record to Update")
options = {
    f"[{row['opportunity_id']}] {row['company_name']} — {row['job_title']}": row['opportunity_id']
    for _, row in df.iterrows()
}
selected_label = st.selectbox("Choose an opportunity", list(options.keys()))
sel_id = options[selected_label]

row_df = get_opportunity_by_id(sel_id)
if row_df.empty:
    st.error("Record not found.")
    st.stop()

row = row_df.iloc[0]

st.subheader("2️⃣ Edit Fields")
st.info("Only fill in the fields you want to change. Leave others as-is.")

with st.form("update_form"):
    col1, col2 = st.columns(2)
    with col1:
        new_status = st.selectbox(
            "Status",
            STATUSES,
            index=STATUSES.index(row["status"]) if row["status"] in STATUSES else 0,
        )
        new_work_mode = st.selectbox(
            "Work Mode",
            WORK_MODES,
            index=WORK_MODES.index(row["work_mode"]) if row["work_mode"] in WORK_MODES else 0,
        )
        new_experience = st.selectbox(
            "Experience Level",
            [""] + EXPERIENCE_LEVELS,
            index=(EXPERIENCE_LEVELS.index(row["experience_level"]) + 1)
            if row["experience_level"] in EXPERIENCE_LEVELS else 0,
        )
    with col2:
        import datetime
        deadline_val = row["application_deadline"]
        if deadline_val and not isinstance(deadline_val, datetime.date):
            try:
                deadline_val = datetime.date.fromisoformat(str(deadline_val))
            except Exception:
                deadline_val = None
        new_deadline = st.date_input("Application Deadline", value=deadline_val)
        new_salary_min = st.number_input("Salary Min", min_value=0.0, step=1000.0,
                                          value=float(row["salary_min"]) if row["salary_min"] else 0.0)
        new_salary_max = st.number_input("Salary Max", min_value=0.0, step=1000.0,
                                          value=float(row["salary_max"]) if row["salary_max"] else 0.0)

    new_skills = st.text_area("Required Skills", value=row["required_skills"] or "")
    new_source  = st.text_input("Source Link", value=row["source_link"] or "")

    submitted = st.form_submit_button("💾 Save Changes", use_container_width=True)

if submitted:
    updates = {
        "status":               new_status,
        "work_mode":            new_work_mode,
        "experience_level":     new_experience or None,
        "application_deadline": new_deadline,
        "salary_min":           new_salary_min if new_salary_min > 0 else None,
        "salary_max":           new_salary_max if new_salary_max > 0 else None,
        "required_skills":      new_skills.strip() or row["required_skills"],
        "source_link":          new_source.strip() or None,
    }
    try:
        success = update_opportunity(sel_id, updates)
        if success:
            st.success(f"✅ Opportunity ID **{sel_id}** updated successfully!")
        else:
            st.warning("No rows were updated. The record may not exist.")
    except Exception as e:
        st.error(f"❌ Update failed: {e}")
