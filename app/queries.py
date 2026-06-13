"""
queries.py  –  All database query functions.
All queries use SQLAlchemy 2.0 text() with bound parameters to prevent SQL injection.
"""
import pandas as pd
from sqlalchemy import text
from app.db import get_engine


# ─────────────────────────────────────────────
# READ
# ─────────────────────────────────────────────

def get_all_opportunities() -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql_query(
            text("SELECT * FROM opportunities ORDER BY created_at DESC"),
            conn,
        )
    return df


def search_opportunities(
    keyword: str = "",
    category: str = "",
    city: str = "",
    work_mode: str = "",
    status: str = "",
    experience_level: str = "",
    salary_min: float = 0,
    salary_max: float = 9_999_999,
) -> pd.DataFrame:
    conditions = ["1=1"]
    params: dict = {}

    if keyword:
        conditions.append(
            "(LOWER(company_name) LIKE :kw OR LOWER(job_title) LIKE :kw "
            "OR LOWER(required_skills) LIKE :kw)"
        )
        params["kw"] = f"%{keyword.lower()}%"
    if category:
        conditions.append("category = :category")
        params["category"] = category
    if city:
        conditions.append("city = :city")
        params["city"] = city
    if work_mode:
        conditions.append("work_mode = :work_mode")
        params["work_mode"] = work_mode
    if status:
        conditions.append("status = :status")
        params["status"] = status
    if experience_level:
        conditions.append("experience_level = :experience_level")
        params["experience_level"] = experience_level

    conditions.append("(salary_max >= :smin OR salary_max IS NULL)")
    params["smin"] = salary_min
    conditions.append("(salary_min <= :smax OR salary_min IS NULL)")
    params["smax"] = salary_max

    sql = f"SELECT * FROM opportunities WHERE {' AND '.join(conditions)} ORDER BY created_at DESC"
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql_query(text(sql), conn, params=params)
    return df


def get_opportunity_by_id(opportunity_id: int) -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql_query(
            text("SELECT * FROM opportunities WHERE opportunity_id = :id"),
            conn,
            params={"id": opportunity_id},
        )
    return df


# ─────────────────────────────────────────────
# CREATE
# ─────────────────────────────────────────────

def insert_opportunity(data: dict) -> int:
    """Insert one opportunity and return the new opportunity_id."""
    sql = text("""
        INSERT INTO opportunities
            (company_name, job_title, category, city, country, work_mode,
             required_skills, salary_min, salary_max, currency,
             experience_level, application_deadline, status, source_link)
        VALUES
            (:company_name, :job_title, :category, :city, :country, :work_mode,
             :required_skills, :salary_min, :salary_max, :currency,
             :experience_level, :application_deadline, :status, :source_link)
        RETURNING opportunity_id
    """)
    engine = get_engine()
    with engine.begin() as conn:
        result = conn.execute(sql, data)
        return result.scalar_one()


def bulk_insert_opportunities(records: list[dict]) -> int:
    """Insert many rows; returns count of rows inserted."""
    if not records:
        return 0
    sql = text("""
        INSERT INTO opportunities
            (company_name, job_title, category, city, country, work_mode,
             required_skills, salary_min, salary_max, currency,
             experience_level, application_deadline, status, source_link)
        VALUES
            (:company_name, :job_title, :category, :city, :country, :work_mode,
             :required_skills, :salary_min, :salary_max, :currency,
             :experience_level, :application_deadline, :status, :source_link)
    """)
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(sql, records)
    return len(records)


# ─────────────────────────────────────────────
# UPDATE
# ─────────────────────────────────────────────

def update_opportunity(opportunity_id: int, updates: dict) -> bool:
    """Update specified fields for a given opportunity_id."""
    if not updates:
        return False
    set_clauses = ", ".join(f"{k} = :{k}" for k in updates)
    sql = text(f"UPDATE opportunities SET {set_clauses} WHERE opportunity_id = :opportunity_id")
    updates["opportunity_id"] = opportunity_id
    engine = get_engine()
    with engine.begin() as conn:
        result = conn.execute(sql, updates)
    return result.rowcount > 0


# ─────────────────────────────────────────────
# DELETE
# ─────────────────────────────────────────────

def delete_opportunity(opportunity_id: int) -> bool:
    engine = get_engine()
    with engine.begin() as conn:
        result = conn.execute(
            text("DELETE FROM opportunities WHERE opportunity_id = :id"),
            {"id": opportunity_id},
        )
    return result.rowcount > 0


# ─────────────────────────────────────────────
# ANALYTICS HELPERS
# ─────────────────────────────────────────────

def get_kpi_summary() -> dict:
    sql = text("""
        SELECT
            COUNT(*)                                        AS total,
            COUNT(*) FILTER (WHERE status = 'Open')         AS open_count,
            COUNT(*) FILTER (WHERE status = 'Closed')       AS closed_count,
            COUNT(*) FILTER (WHERE status = 'Expired')      AS expired_count,
            COUNT(*) FILTER (WHERE status = 'Shortlisted')  AS shortlisted_count,
            COUNT(DISTINCT company_name)                    AS companies,
            COUNT(DISTINCT category)                        AS categories,
            ROUND(AVG((salary_min + salary_max) / 2), 0)    AS avg_salary
        FROM opportunities
    """)
    engine = get_engine()
    with engine.connect() as conn:
        row = conn.execute(sql).mappings().first()
    return dict(row)


def get_category_counts() -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("SELECT category, COUNT(*) AS count FROM opportunities GROUP BY category ORDER BY count DESC"),
            conn,
        )


def get_work_mode_counts() -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("SELECT work_mode, COUNT(*) AS count FROM opportunities GROUP BY work_mode"),
            conn,
        )


def get_status_counts() -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("SELECT status, COUNT(*) AS count FROM opportunities GROUP BY status ORDER BY count DESC"),
            conn,
        )


def get_city_counts() -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("SELECT city, COUNT(*) AS count FROM opportunities GROUP BY city ORDER BY count DESC"),
            conn,
        )


def get_company_counts() -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("SELECT company_name, COUNT(*) AS count FROM opportunities GROUP BY company_name ORDER BY count DESC"),
            conn,
        )


def get_salary_by_category() -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT category,
                       ROUND(AVG(salary_min), 0) AS avg_min,
                       ROUND(AVG(salary_max), 0) AS avg_max
                FROM opportunities
                WHERE salary_min IS NOT NULL AND salary_max IS NOT NULL
                GROUP BY category
                ORDER BY avg_max DESC
            """),
            conn,
        )


def get_skills_frequency() -> pd.DataFrame:
    """Extract individual skills and count their frequency."""
    df = get_all_opportunities()
    if df.empty:
        return pd.DataFrame(columns=["skill", "count"])
    all_skills: list[str] = []
    for skills_str in df["required_skills"].dropna():
        for skill in skills_str.split(","):
            s = skill.strip()
            if s:
                all_skills.append(s)
    skill_series = pd.Series(all_skills)
    counts = skill_series.value_counts().reset_index()
    counts.columns = ["skill", "count"]
    return counts.head(20)


def get_deadline_alerts() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Returns (closing_soon, already_expired) DataFrames."""
    engine = get_engine()
    with engine.connect() as conn:
        closing_soon = pd.read_sql_query(
            text("""
                SELECT * FROM opportunities
                WHERE application_deadline BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
                  AND status = 'Open'
                ORDER BY application_deadline ASC
            """),
            conn,
        )
        expired = pd.read_sql_query(
            text("""
                SELECT * FROM opportunities
                WHERE application_deadline < CURRENT_DATE
                  AND status = 'Open'
                ORDER BY application_deadline ASC
            """),
            conn,
        )
    return closing_soon, expired


def find_duplicates() -> pd.DataFrame:
    """Find probable duplicates by company + title + city."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT company_name, job_title, city, COUNT(*) AS duplicate_count,
                       STRING_AGG(opportunity_id::TEXT, ', ') AS ids
                FROM opportunities
                GROUP BY company_name, job_title, city
                HAVING COUNT(*) > 1
                ORDER BY duplicate_count DESC
            """),
            conn,
        )


def get_table_info() -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = 'opportunities'
                ORDER BY ordinal_position
            """),
            conn,
        )
