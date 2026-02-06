
# ------------------------------------------------------------------------------
# cart_repository.py
# ------------------------------------------------------------------------------
# Repository for accessing Cart records from the database.
# Provides async CRUD methods for carts.
# ------------------------------------------------------------------------------

from typing import List, Optional
from backend.persistance.cart import Cart
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.repositories.base_repository import BaseRepository


class CartRepository(BaseRepository[Cart, int]):
    """Repository for Cart model implementing BaseRepository contract."""
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    UPDATABLE_FIELDS = {"updated_at"}

    async def get(self, id: int) -> Optional[Cart]:
        result = await self.session.execute(
            select(Cart).filter(Cart.cart_id == id)
        )
        return result.scalars().first()

    async def list(self, *, limit: int = 100, offset: int = 0) -> List[Cart]:
        BaseRepository.validate_pagination(limit, offset)
        result = await self.session.execute(
            select(Cart).limit(limit).offset(offset)
        )
        items: List[Cart] = list(result.scalars().all())
        return items

    async def add(self, obj: Cart) -> Cart:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj: Cart) -> Cart:
        existing = await self.get(id)
        if not existing:
            raise ValueError(f"Cart with id {id} not found")
        self.apply_whitelist_update(existing, obj, self.UPDATABLE_FIELDS)
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def delete(self, id: int) -> None:
        existing = await self.get(id)
        if existing:
            await self.soft_delete(existing)
        return None
