


"""
seller_payout_repository.py

Repository class for managing SellerPayout entities in the database.
Provides async method for retrieving seller payouts by ID.
"""

from typing import Optional, List
from backend.persistance.seller_payout import SellerPayout
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.repositories.base_repository import BaseRepository


class SellerPayoutRepository(BaseRepository[SellerPayout, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    UPDATABLE_FIELDS = {"amount", "currency", "status", "date_of_payment"}

    async def get(self, id: int) -> Optional[SellerPayout]:
        result = await self.session.execute(
            select(SellerPayout).filter(SellerPayout.payout_id == id, SellerPayout.is_deleted == False)
        )
        return result.scalars().first()

    async def list(self, *, limit: int = 100, offset: int = 0) -> List[SellerPayout]:
        BaseRepository.validate_pagination(limit, offset)
        result = await self.session.execute(
            select(SellerPayout).filter(SellerPayout.is_deleted == False).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def add(self, obj: SellerPayout) -> SellerPayout:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj: SellerPayout) -> SellerPayout:
        existing = await self.get(id)
        if not existing:
            raise ValueError(f"SellerPayout with id {id} not found")
        self.apply_whitelist_update(existing, obj, self.UPDATABLE_FIELDS)
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def delete(self, id: int) -> None:
        existing = await self.get(id)
        if existing:
            await self.soft_delete(existing)
        return None

    # Service layer compatibility
    async def save(self, obj: SellerPayout) -> SellerPayout:
        """Alias for add() to match service layer expectations."""
        return await self.add(obj)
