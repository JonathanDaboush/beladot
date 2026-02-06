
# ------------------------------------------------------------------------------
# employee_repository.py
# ------------------------------------------------------------------------------
# Repository for accessing Employee records from the database.
# Provides methods for retrieving employees by ID and department.
# ------------------------------------------------------------------------------

from typing import Optional, List, Any
from backend.persistance.employee import Employee
from sqlalchemy import select, update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.base_repository import BaseRepository


class EmployeeRepository(BaseRepository[Employee, int]):
    """Repository for Employee model implementing BaseRepository contract."""
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    UPDATABLE_FIELDS = {"notes"}

    async def get(self, id: int) -> Optional[Employee]:
        result = await self.session.execute(select(Employee).where(Employee.emp_id == id))
        return result.scalar_one_or_none()

    async def list(self, *, limit: int = 100, offset: int = 0) -> List[Employee]:
        BaseRepository.validate_pagination(limit, offset)
        result = await self.session.execute(select(Employee).limit(limit).offset(offset))
        return list(result.scalars().all())

    async def add(self, obj: Employee) -> Employee:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj: Employee) -> Employee:
        # If caller wants field-level updates, they can fetch, modify and call update with the modified obj.
        existing = await self.get(id)
        if not existing:
            raise ValueError(f"Employee with id {id} not found")
        self.apply_whitelist_update(existing, obj, self.UPDATABLE_FIELDS)
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def delete(self, id: int) -> None:
        existing = await self.get(id)
        if existing:
            await self.soft_delete(existing)
        return None

    # Backwards-compatible helper
    async def get_all_employees(self, department_id: Optional[int] = None) -> List[Employee]:
        stmt = select(Employee)
        if department_id is not None:
            stmt = stmt.where(Employee.department_id == department_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # Service layer compatibility aliases
    async def get_by_id(self, id: int) -> Optional[Employee]:
        """Alias for get() to match service layer expectations."""
        return await self.get(id)

    async def get_all(self) -> List[Employee]:
        """Get all employees."""
        return await self.list(limit=1000, offset=0)
