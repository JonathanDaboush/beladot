# migrations/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

# --------------------------------------------------
# Ensure backend is importable
# --------------------------------------------------
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

# Import your declarative Base
from backend.db.base import Base  # canonical declarative Base

# Alembic Config object
config = context.config

# Setup Python logging from config
fileConfig(config.config_file_name)

# Metadata for 'autogenerate'
target_metadata = Base.metadata

# --------------------------------------------------
# Offline migration mode
# --------------------------------------------------
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()

# --------------------------------------------------
# Online migration mode
# --------------------------------------------------
def run_migrations_online():
    # Make sure URL is read from environment variable if set
    if os.getenv("DATABASE_URL"):
        url = os.getenv("DATABASE_URL")
        connectable = engine_from_config(
            {"sqlalchemy.url": url},  # simple dict
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    else:
        # fallback to alembic.ini
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )
        with context.begin_transaction():
            context.run_migrations()

# --------------------------------------------------
# Run
# --------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
