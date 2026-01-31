from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, mapped_column
from sqlalchemy import Integer, String
from sqlalchemy.future import select
from pydantic import BaseModel
import asyncio

# 1. Async SQLAlchemy setup
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/dbname"  # <-- Replace with your DB
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

# 3. Sample model
class Item(Base):
    __tablename__ = "items"
    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, index=True)

# 2. FastAPI dependency for session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session  # New session per request, avoids sharing

# 4. Repository/service function
async def create_item(session: AsyncSession, name: str) -> Item:
    item = Item(name=name)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item

# 5. FastAPI app and endpoint
app = FastAPI()

class ItemCreate(BaseModel):
    name: str

@app.post("/items", response_model=ItemCreate)
async def create_item_endpoint(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_item = await create_item(db, item.name)
        return {"name": new_item.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---
# Comments:
# - Each request gets a new AsyncSession via get_db (async generator).
# - Sessions are NOT shared between requests or coroutines.
# - This avoids 'another operation is in progress' errors from asyncpg/SQLAlchemy.
# - Always await DB operations and never store sessions globally or in FastAPI state.
