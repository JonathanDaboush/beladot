
# ------------------------------------------------------------------------------
# cart_item_repository.py
# ------------------------------------------------------------------------------
# Repository for accessing CartItem records from the database.
# Provides async CRUD methods for cart items.
# ------------------------------------------------------------------------------

from typing import List, Optional
from backend.persistance.cart_item import CartItem
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.repositories.base_repository import BaseRepository


class CartItemRepository(BaseRepository[CartItem, int]):
    """Repository for CartItem model implementing BaseRepository contract."""
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    UPDATABLE_FIELDS = {"quantity", "variant_id"}

    async def get(self, id: int) -> Optional[CartItem]:
        result = await self.session.execute(
            select(CartItem).filter(CartItem.cart_item_id == id)
        )
        return result.scalars().first()

    async def list(self, *, limit: int = 100, offset: int = 0) -> List[CartItem]:
        BaseRepository.validate_pagination(limit, offset)
        result = await self.session.execute(
            select(CartItem).limit(limit).offset(offset)
        )
        items: List[CartItem] = list(result.scalars().all())
        return items

    async def add(self, obj: CartItem) -> CartItem:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj: CartItem) -> CartItem:
        existing = await self.get(id)
        if not existing:
            raise ValueError(f"CartItem with id {id} not found")
        self.apply_whitelist_update(existing, obj, self.UPDATABLE_FIELDS)
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def delete(self, id: int) -> None:
        existing = await self.get(id)
        if existing:
            await self.soft_delete(existing)
        return None
