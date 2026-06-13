"""
db.py  –  Database connection layer
Uses SQLAlchemy 2.0 with psycopg2 driver.
Credentials loaded from environment variables (set via Docker Compose or .env).
"""
import os
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()


def get_db_url() -> str:
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "student_opportunities_db")
    user = os.getenv("DB_USER", "app_user")
    password = os.getenv("DB_PASSWORD", "app_password")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


@st.cache_resource(show_spinner=False)
def get_engine():
    """
    Returns a cached SQLAlchemy Engine.
    st.cache_resource ensures a single engine is shared across all sessions
    (connection-pool reuse) rather than opening a new pool per rerun.
    """
    url = get_db_url()
    engine = create_engine(
        url,
        pool_pre_ping=True,       # validates connections before use
        pool_size=5,
        max_overflow=10,
    )
    return engine


def test_connection() -> tuple[bool, str]:
    """Returns (success: bool, message: str)."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()
        return True, version
    except Exception as exc:
        return False, str(exc)
