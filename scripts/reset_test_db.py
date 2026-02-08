"""
reset_test_db.py

Drops and recreates the test database for a clean test run.
Supports both SQLite and PostgreSQL (requires correct credentials).
"""
import os
from sqlalchemy import create_engine, text

# Update these values for your environment
POSTGRES_URL = os.environ.get("TEST_DATABASE_URL", "postgresql+psycopg2://postgres:password@localhost:5432/divina_test")
SQLITE_URL = "sqlite:///test.db"

# Choose which DB to reset
USE_POSTGRES = POSTGRES_URL.startswith("postgresql")
DB_URL = POSTGRES_URL if USE_POSTGRES else SQLITE_URL

engine = create_engine(DB_URL)

if USE_POSTGRES:
    # Drop all tables in Postgres
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
        conn.commit()
    print("Postgres test database schema reset.")
else:
    # Remove SQLite file
    if os.path.exists("test.db"):
        os.remove("test.db")
    print("SQLite test database file removed.")

print("Ready for migrations and clean test run.")
