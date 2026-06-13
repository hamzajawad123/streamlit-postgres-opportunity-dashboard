"""
7_Duplicate_Detection.py  –  Detect duplicate opportunities
"""
import streamlit as st
from app.queries import find_duplicates, get_all_opportunities

st.title("🔁 Duplicate Detection")
st.markdown(
    "This page identifies **probable duplicate opportunities** by grouping records "
    "with identical `company_name`, `job_title`, and `city`."
)

try:
    dupes_df = find_duplicates()
except Exception as e:
    st.error(f"❌ Could not run duplicate check: {e}")
    st.stop()

if dupes_df.empty:
    st.success("✅ No duplicate records found in the database.")
else:
    st.warning(f"⚠️ Found **{len(dupes_df)}** probable duplicate group(s).")
    st.dataframe(dupes_df, use_container_width=True, hide_index=True)

    st.subheader("🔍 Inspect Duplicate Group")
    sel_company = st.selectbox("Select Company", dupes_df["company_name"].unique())
    sel_title   = st.selectbox(
        "Select Job Title",
        dupes_df[dupes_df["company_name"] == sel_company]["job_title"].unique(),
    )

    try:
        all_df = get_all_opportunities()
        group_df = all_df[
            (all_df["company_name"] == sel_company) &
            (all_df["job_title"]    == sel_title)
        ]
        st.dataframe(group_df, use_container_width=True, hide_index=True)
        st.caption(
            "💡 To remove a duplicate, go to **Delete Opportunity** and select the ID to remove."
        )
    except Exception as e:
        st.error(str(e))

st.divider()
st.markdown("""
### How duplicates are detected
Records are grouped by `company_name` + `job_title` + `city`.
Any group with **more than 1 record** is flagged as a potential duplicate.
The IDs of all records in each group are shown so you can decide which to keep.
""")
