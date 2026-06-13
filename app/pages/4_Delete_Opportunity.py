"""
4_Delete_Opportunity.py  –  Delete an opportunity with preview & confirmation (Admin only)
"""
import streamlit as st
from app.auth import require_admin
from app.queries import get_all_opportunities, get_opportunity_by_id, delete_opportunity

require_admin()

st.title("🗑️ Delete Opportunity")
st.warning("⚠️ Deletion is permanent and cannot be undone.")

try:
    df = get_all_opportunities()
except Exception as e:
    st.error(f"❌ Could not load records: {e}")
    st.stop()

if df.empty:
    st.info("No opportunities in the database.")
    st.stop()

# ── Select record ─────────────────────────────────────────────
options = {
    f"[{row['opportunity_id']}] {row['company_name']} — {row['job_title']}": row['opportunity_id']
    for _, row in df.iterrows()
}
selected_label = st.selectbox("Select an opportunity to delete", list(options.keys()))
sel_id = options[selected_label]

# ── Show preview ──────────────────────────────────────────────
row_df = get_opportunity_by_id(sel_id)
if row_df.empty:
    st.error("Record not found.")
    st.stop()

row = row_df.iloc[0]
st.subheader("📋 Record Preview")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**ID:** `{row['opportunity_id']}`")
    st.markdown(f"**Company:** {row['company_name']}")
    st.markdown(f"**Job Title:** {row['job_title']}")
    st.markdown(f"**Category:** {row['category']}")
    st.markdown(f"**Location:** {row.get('city', 'N/A')} — {row.get('country', 'N/A')}")
with col2:
    st.markdown(f"**Work Mode:** {row['work_mode']}")
    st.markdown(f"**Status:** {row['status']}")
    st.markdown(f"**Deadline:** {row.get('application_deadline', 'N/A')}")
    st.markdown(f"**Created At:** {row.get('created_at', 'N/A')}")

st.divider()

# ── Confirmation ──────────────────────────────────────────────
confirm = st.checkbox(f"I confirm I want to permanently delete record ID **{sel_id}**")
if st.button("🗑️ Delete Record", disabled=not confirm, type="primary"):
    try:
        success = delete_opportunity(sel_id)
        if success:
            st.success(f"✅ Record ID **{sel_id}** deleted successfully.")
            st.rerun()
        else:
            st.warning("Record not found or already deleted.")
    except Exception as e:
        st.error(f"❌ Deletion failed: {e}")
