"""
auth.py  –  Basic login / access control using Streamlit session_state.
Two roles:
  - admin   → can Add, Update, Delete, Upload CSV
  - viewer  → read-only (View, Analytics, Export, Health Check)
Passwords are stored as plain strings here for demo purposes.
In production replace with hashed credentials or an external auth service.
"""
import streamlit as st

# Credentials store  {username: {"password": ..., "role": ...}}
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "viewer": {"password": "viewer123", "role": "viewer"},
    "faculty": {"password": "ucp2026", "role": "admin"},
}


def init_auth():
    """Initialise session state keys if not already set."""
    defaults = {
        "logged_in": False,
        "username": "",
        "role": "",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def show_login_form():
    """Render login form and update session state on success."""
    st.title("🔐 Login")
    st.markdown("Please log in to access the Opportunity Dashboard.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        user = USERS.get(username)
        if user and user["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = user["role"]
            st.success(f"Welcome, **{username}**! Role: `{user['role']}`")
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.info(
        "**Demo credentials**\n\n"
        "Admin → `admin` / `admin123`\n\n"
        "Viewer → `viewer` / `viewer123`\n\n"
        "Faculty → `faculty` / `ucp2026`"
    )


def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.rerun()


def require_admin():
    """Call at the top of any admin-only page."""
    if st.session_state.get("role") != "admin":
        st.warning("⛔ This page requires **Admin** privileges.")
        st.stop()


def is_admin() -> bool:
    return st.session_state.get("role") == "admin"
