"""
6_CSV_Upload_Export.py  –  CSV bulk upload (Admin) and export (all roles)
"""
import streamlit as st
import pandas as pd
from app.auth import is_admin
from app.queries import get_all_opportunities, bulk_insert_opportunities
from app.utils import (
    validate_csv_upload, df_to_csv_bytes,
    REQUIRED_CSV_COLUMNS, OPTIONAL_CSV_COLUMNS,
)

st.title("📁 CSV Upload & Export")

tab_upload, tab_export, tab_template = st.tabs(["⬆️ Upload", "⬇️ Export", "📄 Template"])

# ── UPLOAD (Admin only) ───────────────────────────────────────
with tab_upload:
    if not is_admin():
        st.warning("⛔ CSV Upload requires Admin role.")
    else:
        st.markdown("Upload a CSV file to bulk-insert opportunities into PostgreSQL.")
        st.markdown(f"**Required columns:** `{', '.join(REQUIRED_CSV_COLUMNS)}`")
        st.markdown(f"**Optional columns:** `{', '.join(OPTIONAL_CSV_COLUMNS)}`")

        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

        if uploaded_file:
            try:
                df_raw = pd.read_csv(uploaded_file)
            except Exception as e:
                st.error(f"Could not read CSV: {e}")
                st.stop()

            st.subheader("👁️ Preview (first 10 rows)")
            st.dataframe(df_raw.head(10), use_container_width=True)
            st.caption(f"Total rows: **{len(df_raw)}**  |  Columns: **{list(df_raw.columns)}**")

            df_clean, errors = validate_csv_upload(df_raw.copy())

            if errors:
                st.subheader("❌ Validation Errors")
                for err in errors:
                    st.error(err)
                st.warning("Fix the errors above before inserting.")
            else:
                st.success("✅ Validation passed! Ready to insert.")
                if st.button("💾 Insert All Valid Rows into PostgreSQL", use_container_width=True):
                    records = []
                    all_cols = REQUIRED_CSV_COLUMNS + OPTIONAL_CSV_COLUMNS
                    for _, row in df_clean.iterrows():
                        record = {col: (row.get(col) if pd.notna(row.get(col)) else None) for col in all_cols}
                        records.append(record)
                    try:
                        count = bulk_insert_opportunities(records)
                        st.success(f"✅ Successfully inserted **{count}** records!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Insert failed: {e}")

# ── EXPORT ────────────────────────────────────────────────────
with tab_export:
    st.markdown("Export current database records as a CSV file.")

    col1, col2 = st.columns(2)
    with col1:
        from app.utils import STATUSES, CATEGORIES
        export_status   = st.selectbox("Filter by Status",   ["All"] + STATUSES,    key="exp_status")
        export_category = st.selectbox("Filter by Category", ["All"] + CATEGORIES,  key="exp_cat")
    with col2:
        export_city = st.text_input("Filter by City (optional)", key="exp_city")

    try:
        df_all = get_all_opportunities()
        if export_status != "All":
            df_all = df_all[df_all["status"] == export_status]
        if export_category != "All":
            df_all = df_all[df_all["category"] == export_category]
        if export_city.strip():
            df_all = df_all[df_all["city"].str.lower() == export_city.strip().lower()]

        st.info(f"**{len(df_all)}** records will be exported.")
        st.dataframe(df_all.head(5), use_container_width=True)

        st.download_button(
            label="📥 Download as CSV",
            data=df_to_csv_bytes(df_all),
            file_name="opportunities_export.csv",
            mime="text/csv",
            use_container_width=True,
        )
    except Exception as e:
        st.error(f"❌ Export failed: {e}")

# ── TEMPLATE ──────────────────────────────────────────────────
with tab_template:
    st.markdown("Download a blank CSV template with the correct column headers.")
    template_df = pd.DataFrame(columns=REQUIRED_CSV_COLUMNS + OPTIONAL_CSV_COLUMNS)
    # Add one example row
    template_df.loc[0] = {
        "company_name": "Example Corp",
        "job_title":    "Data Science Intern",
        "category":     "Data Science",
        "work_mode":    "Hybrid",
        "required_skills": "Python, SQL, pandas",
        "status":       "Open",
        "city":         "Lahore",
        "country":      "Pakistan",
        "salary_min":   40000,
        "salary_max":   60000,
        "currency":     "PKR",
        "experience_level": "Entry Level",
        "application_deadline": "2026-08-01",
        "source_link":  "https://example.com/jobs",
    }
    st.dataframe(template_df, use_container_width=True)
    st.download_button(
        label="📥 Download Template CSV",
        data=df_to_csv_bytes(template_df),
        file_name="upload_template.csv",
        mime="text/csv",
        use_container_width=True,
    )
