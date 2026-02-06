"""
Utilities to initialize the database schema in a deterministic order.

- Dynamically imports all ORM model modules under `backend.persistance` so
  SQLAlchemy `Base.metadata` includes every table and foreign key.
- Provides functions to create or reset the schema for dev/test SQLite and
  other environments using the configured sync engine.

Use cases:
- Tests: call `init_test_schema()` to drop/create all tables on the test DB.
- Dev app startup: call `ensure_sqlite_schema()` to create missing tables
  when running locally on SQLite.
"""

from sqlalchemy.engine import Engine
import importlib
import pkgutil

from backend.db.base import Base
from backend.persistance.base import get_engine


def _import_all_persistance_models() -> None:
    """Import all modules in backend.persistance to register ORM tables.

    SQLAlchemy creates tables in correct dependency order automatically, but
    only after all table metadata is present. This function ensures that by
    importing every module within `backend.persistance`.
    """
    package_name = "backend.persistance"
    package = importlib.import_module(package_name)
    for _, mod_name, is_pkg in pkgutil.iter_modules(package.__path__):
        # Skip subpackages; most ORM models are top-level modules
        if is_pkg:
            continue
        try:
            importlib.import_module(f"{package_name}.{mod_name}")
        except Exception as e:
            try:
                from backend.infrastructure.structured_logging import logger
                logger.exception("init_schema.import_failed", module=mod_name, error=str(e))
            except Exception:
                pass


def init_schema(engine: Engine | None = None, drop: bool = False) -> None:
    """Initialize the schema on the provided engine.

    - Imports all model modules
    - Optionally drops existing tables
    - Creates all tables in FK-safe order
    """
    _import_all_persistance_models()
    if engine is None:
        engine = get_engine()
    if drop:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def init_test_schema() -> None:
    """Reset the test database schema to a clean state.

    Intended for pytest fixtures: drops then creates all tables.
    """
    engine = get_engine()
    init_schema(engine, drop=True)


def ensure_sqlite_schema() -> None:
    """Ensure local SQLite schema exists by creating any missing tables.

    Safe to call at app startup in dev/test; operation is idempotent.
    """
    engine = get_engine()
    _import_all_persistance_models()
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    # CLI utility: initialize dev schema (non-destructive by default)
    import argparse
    parser = argparse.ArgumentParser(description="Initialize DB schema")
    parser.add_argument("--drop", action="store_true", help="Drop all tables before creating")
    args = parser.parse_args()
    init_schema(drop=args.drop)
    print("Schema initialized.")
