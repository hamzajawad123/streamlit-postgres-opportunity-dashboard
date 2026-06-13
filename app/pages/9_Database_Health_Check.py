"""
9_Database_Health_Check.py  –  Database connection and health diagnostics
"""
import streamlit as st
from app.db import test_connection, get_db_url
from app.queries import get_all_opportunities, get_table_info
import os

st.title("🩺 Database Health Check")
st.markdown("Verify the PostgreSQL connection, table structure, and data integrity.")

# ── Connection test ───────────────────────────────────────────
st.subheader("1️⃣ Connection Status")
if st.button("🔌 Test Database Connection", use_container_width=True):
    with st.spinner("Connecting to PostgreSQL..."):
        ok, msg = test_connection()
    if ok:
        st.success("✅ Connection successful!")
        st.code(f"PostgreSQL Version: {msg}", language="text")
    else:
        st.error(f"❌ Connection failed: {msg}")
        st.info(
            "**Troubleshooting tips:**\n"
            "- Ensure `docker compose up -d` is running\n"
            "- Check DB_HOST, DB_PORT, DB_USER, DB_PASSWORD environment variables\n"
            "- Run: `docker compose logs postgres_db`"
        )

# ── Environment vars ──────────────────────────────────────────
st.subheader("2️⃣ Environment Configuration")
col1, col2 = st.columns(2)
with col1:
    st.metric("DB Host",     os.getenv("DB_HOST", "not set"))
    st.metric("DB Port",     os.getenv("DB_PORT", "not set"))
    st.metric("DB Name",     os.getenv("DB_NAME", "not set"))
with col2:
    st.metric("DB User",     os.getenv("DB_USER", "not set"))
    st.metric("DB Password", "***" if os.getenv("DB_PASSWORD") else "not set")

# ── Row count ─────────────────────────────────────────────────
st.subheader("3️⃣ Table Statistics")
try:
    df = get_all_opportunities()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Rows",   len(df))
    c2.metric("Companies",    df["company_name"].nunique() if not df.empty else 0)
    c3.metric("Open Records", len(df[df["status"] == "Open"]) if not df.empty else 0)

    if not df.empty:
        st.markdown("**Latest Record:**")
        st.dataframe(df.head(1), use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Could not query table: {e}")

# ── Table schema ──────────────────────────────────────────────
st.subheader("4️⃣ Table Schema — opportunities")
try:
    schema_df = get_table_info()
    st.dataframe(schema_df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Could not retrieve schema: {e}")

# ── pgAdmin guide ─────────────────────────────────────────────
st.subheader("5️⃣ pgAdmin Verification Guide")
with st.expander("How to connect pgAdmin to this PostgreSQL instance"):
    st.markdown("""
    1. Open **http://localhost:5050** in your browser
    2. Login: `admin@example.com` / `admin123`
    3. Click **Add New Server**
    4. **General tab** → Name: `Opportunity DB`
    5. **Connection tab:**
       - Host: `postgres_db` *(service name inside Docker network)*
       - Port: `5432`
       - Database: `student_opportunities_db`
       - Username: `app_user`
       - Password: `app_password`
    6. Click **Save** — you should see the database appear in the left panel
    """)

with st.expander("Useful SQL queries to run in pgAdmin"):
    st.code("""
-- All records
SELECT * FROM opportunities;

-- Count by category
SELECT category, COUNT(*) FROM opportunities GROUP BY category;

-- Count by work mode
SELECT work_mode, COUNT(*) FROM opportunities GROUP BY work_mode;

-- Open opportunities
SELECT * FROM opportunities WHERE status = 'Open';

-- Closing soon
SELECT * FROM opportunities
WHERE application_deadline <= CURRENT_DATE + INTERVAL '7 days';

-- Total count
SELECT COUNT(*) FROM opportunities;
    """, language="sql")
