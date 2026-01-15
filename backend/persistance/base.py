
# ------------------------------------------------------------------------------
# base.py
# ------------------------------------------------------------------------------
# Defines the declarative base class for all SQLAlchemy ORM models in the
# persistence layer. All ORM models should inherit from this Base class.
# ------------------------------------------------------------------------------

from sqlalchemy.orm import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from backend.config import settings
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for all ORM models.
Base = declarative_base()
