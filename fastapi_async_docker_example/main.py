import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, mapped_column
from sqlalchemy import Integer, String

from pydantic import BaseModel

# 3. Database URL construction for dev/test
DB_USER = "appuser"
DB_PASS = "password"
DB_HOST = "localhost"
DB_NAME = "app_dev"
DB_PORT = 5432



DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 2. Async SQLAlchemy setup
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

# 4. Sample model
class Item(Base):
    __tablename__ = "items"
    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, index=True)

# 2. FastAPI dependency for session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session  # New session per request, avoids sharing

# 5. Repository/service function
async def create_item(session: AsyncSession, name: str) -> Item:
    item = Item(name=name)
    session.add(item)
    try:
        await session.commit()
        await session.refresh(item)
        return item
    except Exception:
        await session.rollback()
        raise

# 6. FastAPI app and endpoint

from contextlib import asynccontextmanager

# 1. Lifespan handler replaces startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: create tables if needed
    if os.getenv("TESTING") == "1":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield  # App runs here
    # Shutdown code: nothing needed, but you could clean up here

app = FastAPI(lifespan=lifespan)


class ItemCreate(BaseModel):
    name: str

@app.post("/items", response_model=ItemCreate)
async def create_item_endpoint(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_item = await create_item(db, item.name)
        return {"name": new_item.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6. Comments:
# - The @asynccontextmanager lifespan handler replaces deprecated startup/shutdown events.
# - Each request gets a new AsyncSession via get_db (async generator), so sessions are never shared.
# - This avoids asyncpg 'another operation in progress' errors by ensuring no session is reused across awaits.

# 8. Comments:
# - Separate dev/test DBs (docker-compose) prevent collisions and InterfaceError.
# - Each request gets a new AsyncSession via get_db (async generator).
# - Table creation on test startup prevents 500 errors in tests.
