"""
0_Home.py  –  Home / Introduction page
"""
import streamlit as st

st.title("🎓 Internship & Job Tracking Dashboard")
st.subheader("University of Central Punjab — Tools & Techniques for Data Science")
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## 📋 Project Overview
    This application is a **Student Opportunity Management System** built for the UCP
    Department of Applied Computing & Technologies.

    Faculty and students can:
    - 📥 **Add** new internship and job opportunities
    - 🔍 **Search & Filter** records by multiple criteria
    - ✏️ **Update** opportunity details and statuses
    - 🗑️ **Delete** invalid records
    - 📊 **Analyse** trends, salaries, and top skills
    - 📁 **Upload** bulk data via CSV
    - 📤 **Export** filtered results as CSV
    - ⏰ **Track deadlines** and get alerts
    - 🔁 **Detect duplicates** before inserting data
    """)

with col2:
    st.markdown("## 🛠️ Tech Stack")
    st.markdown("""
    | Layer | Technology |
    |-------|-----------|
    | Frontend | Streamlit |
    | Database | PostgreSQL |
    | DB Admin | pgAdmin 4 |
    | ORM | SQLAlchemy 2.0 |
    | Charts | Plotly |
    | Container | Docker Compose |
    | Language | Python 3.11 |
    """)

st.divider()

st.markdown("## 🏗️ System Architecture")
st.code("""
User Browser
     │
     ▼
Streamlit App Container  (port 8501)
     │
     ▼
PostgreSQL Container     (port 5432)  ◄────► pgAdmin Container (port 5050)
     │
     ▼
Docker Named Volume  (postgres_data)  ← Persistent storage

GitHub Repository  →  Source code, commits, documentation
""", language="text")

st.divider()

st.markdown("## 👥 Team Members")
team_data = {
    "Name": ["Hamza Jawad", "Muhammad Ahmad", "Sumain Ahmad", "Abdul Moiz"],
    "GitHub Username": ["@hamzajawad123", "@muh-ahmad28", "@Sumain1122", "Coder27102004"],
    "Contributions": [
        "DB schema, seed data, queries.py",
        "Streamlit pages, analytics, CSV upload",
        "Docker Compose, Dockerfile, README, report",
    ],
}
import pandas as pd
st.dataframe(pd.DataFrame(team_data), use_container_width=True, hide_index=True)

st.divider()

st.markdown("## 🚀 Quick Start Guide")
with st.expander("How to run this project locally"):
    st.code("""
# 1. Clone the repository
git clone https://github.com/your-org/streamlit-postgres-assignment.git
cd streamlit-postgres-assignment

# 2. Copy environment file
cp .env.example .env

# 3. Start all services
docker compose up -d

# 4. Open the app
#    Streamlit  → http://localhost:8501
#    pgAdmin    → http://localhost:5050
    """, language="bash")

with st.expander("Default login credentials"):
    st.markdown("""
    | Username | Password | Role |
    |----------|----------|------|
    | `admin`   | `admin123`  | Admin (full access) |
    | `viewer`  | `viewer123` | Viewer (read-only)  |
    | `faculty` | `ucp2026`   | Admin (full access) |
    """)
