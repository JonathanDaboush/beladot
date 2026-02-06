"""
seller_component_repository.py

Repository class for managing SellerComponent entities in the database.
Provides async CRUD operations for seller components.
"""

from typing import Optional, List
from backend.persistance.seller_component import SellerComponent
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.repositories.base_repository import BaseRepository


class SellerComponentRepository(BaseRepository[SellerComponent, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    UPDATABLE_FIELDS = {"img_url", "description"}

    async def get(self, id: int) -> Optional[SellerComponent]:
        result = await self.session.execute(select(SellerComponent).filter(SellerComponent.id == id))
        return result.scalars().first()

    async def list(self, *, limit: int = 100, offset: int = 0) -> List[SellerComponent]:
        BaseRepository.validate_pagination(limit, offset)
        result = await self.session.execute(select(SellerComponent).limit(limit).offset(offset))
        return list(result.scalars().all())

    async def add(self, obj: SellerComponent) -> SellerComponent:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj: SellerComponent) -> SellerComponent:
        existing = await self.get(id)
        if not existing:
            raise ValueError(f"SellerComponent with id {id} not found")
        self.apply_whitelist_update(existing, obj, self.UPDATABLE_FIELDS)
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def delete(self, id: int) -> None:
        existing = await self.get(id)
        if existing:
            await self.soft_delete(existing)
        return None

    async def create(self, img_url: str, description: str) -> SellerComponent:
        component = SellerComponent(img_url=img_url, description=description)
        self.session.add(component)
        await self.session.commit()
        await self.session.refresh(component)
        return component

    async def get_all(self) -> List[SellerComponent]:
        """Get all seller components."""
        return await self.list(limit=1000, offset=0)

    async def get_by_id(self, id: int) -> Optional[SellerComponent]:
        """Get seller component by ID."""
        return await self.get(id)
