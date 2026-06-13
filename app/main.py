"""
main.py  –  Entrypoint for the Streamlit multipage app.
Uses st.navigation (Streamlit's modern multipage API) with login gate.
"""
import streamlit as st
from app.auth import init_auth, show_login_form, logout, is_admin

st.set_page_config(
    page_title="Opportunity Dashboard | UCP",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_auth()

# ── If not logged in, show login page only ────────────────────
if not st.session_state.logged_in:
    show_login_form()
    st.stop()

# ── Sidebar user info & logout ────────────────────────────────
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.username}")
    st.caption(f"Role: `{st.session_state.role}`")
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        logout()

# ── Define pages ──────────────────────────────────────────────
home_page   = st.Page("pages/0_Home.py",                   title="🏠 Home",               default=True)
view_page   = st.Page("pages/2_View_Search.py",            title="🔍 View & Search")
analytics   = st.Page("pages/5_Analytics_Dashboard.py",    title="📊 Analytics Dashboard")
export_page = st.Page("pages/6_CSV_Upload_Export.py",      title="📁 CSV Upload / Export")
dupes_page  = st.Page("pages/7_Duplicate_Detection.py",    title="🔁 Duplicate Detection")
alerts_page = st.Page("pages/8_Deadline_Alerts.py",        title="⏰ Deadline Alerts")
health_page = st.Page("pages/9_Database_Health_Check.py",  title="🩺 DB Health Check")

# Admin-only pages
add_page    = st.Page("pages/1_Add_Opportunity.py",        title="➕ Add Opportunity")
update_page = st.Page("pages/3_Update_Opportunity.py",     title="✏️ Update Opportunity")
delete_page = st.Page("pages/4_Delete_Opportunity.py",     title="🗑️ Delete Opportunity")

if is_admin():
    nav = st.navigation({
        "General":    [home_page, view_page, analytics, alerts_page, dupes_page],
        "Data Entry": [add_page, update_page, delete_page, export_page],
        "System":     [health_page],
    })
else:
    nav = st.navigation({
        "General": [home_page, view_page, analytics, alerts_page, dupes_page, export_page],
        "System":  [health_page],
    })

nav.run()
