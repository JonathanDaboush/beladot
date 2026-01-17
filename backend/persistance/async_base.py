# Async SQLAlchemy setup for FastAPI/Quart

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker  # retained for compatibility where imported
import os

SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set")

# Create async engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

# Async session factory (typed)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)



