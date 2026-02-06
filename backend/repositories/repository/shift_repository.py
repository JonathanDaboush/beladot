



"""
shift_repository.py

Repository class for managing Shift entities in the database.
Provides async methods for retrieving shifts by ID and by employee/time range.
"""

from typing import Optional, List
from backend.persistance.shift import Shift
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.repositories.base_repository import BaseRepository


class ShiftRepository(BaseRepository[Shift, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    UPDATABLE_FIELDS = {"start_time", "end_time", "notes", "status"}

    async def get(self, id: int) -> Optional[Shift]:
        result = await self.session.execute(select(Shift).where(Shift.shift_id == id))
        return result.scalars().first()

    async def list(self, *, limit: int = 100, offset: int = 0) -> List[Shift]:
        BaseRepository.validate_pagination(limit, offset)
        result = await self.session.execute(select(Shift).limit(limit).offset(offset))
        return list(result.scalars().all())

    async def add(self, obj: Shift) -> Shift:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj: Shift) -> Shift:
        existing = await self.get(id)
        if not existing:
            raise ValueError(f"Shift with id {id} not found")
        self.apply_whitelist_update(existing, obj, self.UPDATABLE_FIELDS)
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def delete(self, id: int) -> None:
        existing = await self.get(id)
        if existing:
            await self.soft_delete(existing)
        return None

    # Service layer compatibility methods
    async def get_by_id(self, id: int) -> Optional[Shift]:
        """Alias for get() to match service layer expectations."""
        return await self.get(id)

    async def save(self, obj: Shift) -> Shift:
        """Alias for add() to match service layer expectations."""
        return await self.add(obj)

    async def get_shifts_by_employee_and_time(self, employee_id: int, start_time, end_time) -> List[Shift]:
        result = await self.session.execute(
            select(Shift).where(
                Shift.emp_id == employee_id,
                Shift.start_time >= start_time,
                Shift.end_time <= end_time
            )
        )
        return list(result.scalars().all())
