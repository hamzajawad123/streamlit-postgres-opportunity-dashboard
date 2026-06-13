"""
8_Deadline_Alerts.py  –  Show opportunities closing within 7 days and expired ones
"""
import streamlit as st
from app.queries import get_deadline_alerts

st.title("⏰ Deadline Alerts")
st.markdown("Stay on top of upcoming and expired opportunities.")

try:
    closing_soon, expired = get_deadline_alerts()
except Exception as e:
    st.error(f"❌ Could not load deadline data: {e}")
    st.stop()

# ── Closing soon ──────────────────────────────────────────────
st.subheader(f"🚨 Closing Within 7 Days ({len(closing_soon)} records)")
if closing_soon.empty:
    st.success("✅ No opportunities closing in the next 7 days.")
else:
    cols_to_show = ["opportunity_id", "company_name", "job_title", "category",
                    "city", "work_mode", "application_deadline", "status"]
    existing = [c for c in cols_to_show if c in closing_soon.columns]
    st.dataframe(closing_soon[existing], use_container_width=True, hide_index=True)

st.divider()

# ── Expired (still Open status) ───────────────────────────────
st.subheader(f"🟠 Past Deadline but Still 'Open' ({len(expired)} records)")
if expired.empty:
    st.success("✅ No expired-but-open records found.")
else:
    st.warning(
        "The following opportunities are past their deadline but still marked as **Open**. "
        "Consider updating their status to **Expired**."
    )
    existing2 = [c for c in ["opportunity_id", "company_name", "job_title",
                              "application_deadline", "status"] if c in expired.columns]
    st.dataframe(expired[existing2], use_container_width=True, hide_index=True)

    if st.button("🔄 Mark All Expired Records as 'Expired'"):
        from app.queries import update_opportunity
        from app.auth import is_admin
        if not is_admin():
            st.warning("⛔ Admin role required to update records.")
        else:
            updated = 0
            for oid in expired["opportunity_id"].tolist():
                try:
                    update_opportunity(oid, {"status": "Expired"})
                    updated += 1
                except Exception:
                    pass
            st.success(f"✅ Marked **{updated}** records as Expired.")
            st.rerun()
