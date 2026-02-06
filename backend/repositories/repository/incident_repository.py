
# ------------------------------------------------------------------------------
# incident_repository.py
# ------------------------------------------------------------------------------
# Repository for accessing Incident records from the database.
# Provides CRUD methods for incidents, including soft delete.
# ------------------------------------------------------------------------------

from typing import Optional, List
from backend.persistance.incident import Incident
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.base_repository import BaseRepository


class IncidentRepository(BaseRepository[Incident, int]):
    """Repository for Incident model implementing BaseRepository contract."""
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    UPDATABLE_FIELDS = {"description", "cost", "date", "status", "status_addressed", "paid_all"}

    async def get(self, id: int) -> Optional[Incident]:
        result = await self.session.execute(select(Incident).where(Incident.incident_id == id, Incident.is_deleted == False))
        return result.scalar_one_or_none()

    async def list(self, *, limit: int = 100, offset: int = 0) -> List[Incident]:
        BaseRepository.validate_pagination(limit, offset)
        result = await self.session.execute(select(Incident).where(Incident.is_deleted == False).limit(limit).offset(offset))
        items: List[Incident] = list(result.scalars().all())
        return items

    async def add(self, obj: Incident) -> Incident:
        self.session.add(obj)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj: Incident) -> Incident:
        existing = await self.get(id)
        if not existing:
            raise ValueError(f"Incident with id {id} not found")
        self.apply_whitelist_update(existing, obj, self.UPDATABLE_FIELDS)
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def delete(self, id: int) -> None:
        existing = await self.get(id)
        if existing:
            existing.is_deleted = True
            await self.session.commit()
        return None

    async def get_all(self) -> List[Incident]:
        stmt = select(Incident).where(Incident.is_deleted == False)
        result = await self.session.execute(stmt)
        items: List[Incident] = list(result.scalars().all())
        return items

    # Service layer compatibility aliases
    async def get_by_id(self, id: int) -> Optional[Incident]:
        """Alias for get() to match service layer expectations."""
        return await self.get(id)

    async def save(self, obj: Incident) -> Incident:
        """Alias for add() to match service layer expectations."""
        return await self.add(obj)
