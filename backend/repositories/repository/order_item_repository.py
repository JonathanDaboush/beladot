
# ------------------------------------------------------------------------------
# order_item_repository.py
# ------------------------------------------------------------------------------
# Repository for accessing OrderItem records from the database.
# Provides async CRUD methods for order items.
# ------------------------------------------------------------------------------

from typing import Optional, List
from backend.persistance.order_item import OrderItem
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.repositories.base_repository import BaseRepository


class OrderItemRepository(BaseRepository[OrderItem, int]):
    """Repository for OrderItem model implementing BaseRepository contract."""
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    UPDATABLE_FIELDS = {"quantity", "subtotal", "variant_id"}

    async def get(self, id: int) -> Optional[OrderItem]:
        result = await self.session.execute(select(OrderItem).filter(OrderItem.order_item_id == id))
        return result.scalars().first()

    async def list(self, *, limit: int = 100, offset: int = 0) -> List[OrderItem]:
        BaseRepository.validate_pagination(limit, offset)
        result = await self.session.execute(select(OrderItem).limit(limit).offset(offset))
        return list(result.scalars().all())

    async def add(self, obj: OrderItem) -> OrderItem:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj: OrderItem) -> OrderItem:
        existing = await self.get(id)
        if not existing:
            raise ValueError(f"OrderItem with id {id} not found")
        self.apply_whitelist_update(existing, obj, self.UPDATABLE_FIELDS)
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def delete(self, id: int) -> None:
        existing = await self.get(id)
        if existing:
            await self.soft_delete(existing)
        return None

    async def get_by_order_id(self, order_id: int) -> List[OrderItem]:
        result = await self.session.execute(select(OrderItem).filter(OrderItem.order_id == order_id))
        return list(result.scalars().all())
