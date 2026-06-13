"""
utils.py  –  Shared helper utilities for the Streamlit app.
"""
import io
import pandas as pd
import streamlit as st

# ── Dropdown option lists ─────────────────────────────────────
CATEGORIES = ["Data Science", "AI", "Web Development", "Cyber Security", "Software Engineering"]
WORK_MODES = ["Remote", "Onsite", "Hybrid"]
STATUSES   = ["Open", "Closed", "Expired", "Shortlisted"]
EXPERIENCE_LEVELS = ["Entry Level", "Mid Level", "Senior Level"]
CURRENCIES = ["PKR", "USD", "EUR", "GBP"]

# Required columns for CSV upload
REQUIRED_CSV_COLUMNS = [
    "company_name", "job_title", "category", "work_mode",
    "required_skills", "status",
]

OPTIONAL_CSV_COLUMNS = [
    "city", "country", "salary_min", "salary_max", "currency",
    "experience_level", "application_deadline", "source_link",
]


def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert DataFrame to UTF-8 CSV bytes for st.download_button."""
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")


def validate_csv_upload(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """
    Validate an uploaded CSV.
    Returns (cleaned_df, list_of_error_messages).
    Error list is empty if the data is valid.
    """
    errors: list[str] = []
    missing_cols = [c for c in REQUIRED_CSV_COLUMNS if c not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {', '.join(missing_cols)}")
        return df, errors

    # Fill optional columns with None
    for col in OPTIONAL_CSV_COLUMNS:
        if col not in df.columns:
            df[col] = None

    # Validate category
    invalid_cat = df[~df["category"].isin(CATEGORIES + [None, ""])]
    if not invalid_cat.empty:
        errors.append(
            f"Row(s) {list(invalid_cat.index + 2)} have invalid category. "
            f"Allowed: {CATEGORIES}"
        )

    # Validate work_mode
    invalid_wm = df[~df["work_mode"].isin(WORK_MODES + [None, ""])]
    if not invalid_wm.empty:
        errors.append(
            f"Row(s) {list(invalid_wm.index + 2)} have invalid work_mode. "
            f"Allowed: {WORK_MODES}"
        )

    # Validate status
    invalid_st = df[~df["status"].isin(STATUSES + [None, ""])]
    if not invalid_st.empty:
        errors.append(
            f"Row(s) {list(invalid_st.index + 2)} have invalid status. "
            f"Allowed: {STATUSES}"
        )

    return df, errors


def display_no_data_message(context: str = ""):
    st.info(f"No records found{' for ' + context if context else ''}.")


def format_salary(salary_min, salary_max, currency="PKR") -> str:
    if salary_min and salary_max:
        return f"{currency} {int(salary_min):,} – {int(salary_max):,}"
    elif salary_min:
        return f"{currency} {int(salary_min):,}+"
    return "Not specified"


def status_badge(status: str) -> str:
    colors = {
        "Open": "🟢",
        "Closed": "🔴",
        "Expired": "🟠",
        "Shortlisted": "🔵",
    }
    return f"{colors.get(status, '⚪')} {status}"
