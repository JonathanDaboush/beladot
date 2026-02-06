

"""
reimbursement_repository.py

Repository class for managing Reimbursement entities in the database.
Provides async CRUD operations and incident-based queries for reimbursements.
"""

from typing import Optional, List
from backend.persistance.reimbursement import Reimbursement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.repositories.base_repository import BaseRepository


class ReimbursementRepository(BaseRepository[Reimbursement, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    UPDATABLE_FIELDS = {"description", "response", "amount_approved", "status", "status_addressed", "paid_all"}

    async def get(self, id: int) -> Optional[Reimbursement]:
        result = await self.session.execute(select(Reimbursement).filter(Reimbursement.reimbursement_id == id))
        return result.scalars().first()

    async def list(self, *, limit: int = 100, offset: int = 0) -> List[Reimbursement]:
        BaseRepository.validate_pagination(limit, offset)
        result = await self.session.execute(select(Reimbursement).limit(limit).offset(offset))
        return list(result.scalars().all())

    async def add(self, obj: Reimbursement) -> Reimbursement:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj: Reimbursement) -> Reimbursement:
        existing = await self.get(id)
        if not existing:
            raise ValueError(f"Reimbursement with id {id} not found")
        self.apply_whitelist_update(existing, obj, self.UPDATABLE_FIELDS)
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def delete(self, id: int) -> None:
        existing = await self.get(id)
        if existing:
            await self.soft_delete(existing)
        return None

    async def get_by_incident_id(self, incident_id: int) -> List[Reimbursement]:
        result = await self.session.execute(
            select(Reimbursement).filter(Reimbursement.incident_id == incident_id)
        )
        return list(result.scalars().all())

    # Service layer compatibility aliases
    async def get_by_id(self, id: int) -> Optional[Reimbursement]:
        """Alias for get() to match service layer expectations."""
        return await self.get(id)

    async def get_all(self) -> List[Reimbursement]:
        """Get all reimbursements."""
        return await self.list(limit=1000, offset=0)

    async def save(self, obj: Reimbursement) -> Reimbursement:
        """Alias for add() to match service layer expectations."""
        return await self.add(obj)
