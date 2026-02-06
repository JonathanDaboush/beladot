
# ------------------------------------------------------------------------------
# employee_component_repository.py
# ------------------------------------------------------------------------------
# Repository for accessing EmployeeComponent records from the database.
# Provides async CRUD methods for employee components.
# ------------------------------------------------------------------------------

from typing import Optional, List, Any
from backend.persistance.employee_component import EmployeeComponent
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.repositories.base_repository import BaseRepository


class EmployeeComponentRepository(BaseRepository[EmployeeComponent, int]):
    """Repository for EmployeeComponent model implementing BaseRepository contract."""
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    UPDATABLE_FIELDS = {"img_url", "description"}

    async def get(self, id: int) -> Optional[EmployeeComponent]:
        result = await self.session.execute(select(EmployeeComponent).filter(EmployeeComponent.id == id))
        return result.scalars().first()

    async def list(self, *, limit: int = 100, offset: int = 0) -> List[EmployeeComponent]:
        BaseRepository.validate_pagination(limit, offset)
        result = await self.session.execute(select(EmployeeComponent).limit(limit).offset(offset))
        return list(result.scalars().all())

    async def add(self, obj: EmployeeComponent) -> EmployeeComponent:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj: EmployeeComponent) -> EmployeeComponent:
        existing = await self.get(id)
        if not existing:
            raise ValueError(f"EmployeeComponent with id {id} not found")
        self.apply_whitelist_update(existing, obj, self.UPDATABLE_FIELDS)
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def delete(self, id: int) -> None:
        existing = await self.get(id)
        if existing:
            await self.soft_delete(existing)
        return None

    async def create(self, img_url: str, description: str, department_id: int) -> EmployeeComponent:
        component = EmployeeComponent(img_url=img_url, description=description, department_id=department_id)
        self.session.add(component)
        await self.session.commit()
        await self.session.refresh(component)
        return component

    # Service layer compatibility methods
    async def get_all(self) -> List[EmployeeComponent]:
        """Get all employee components."""
        return await self.list(limit=1000, offset=0)

    async def get_by_id(self, id: int) -> Optional[EmployeeComponent]:
        """Alias for get() to match service layer expectations."""
        return await self.get(id)

    async def get_by_department(self, department_id: int) -> List[EmployeeComponent]:
        """Get employee components for a specific department."""
        result = await self.session.execute(select(EmployeeComponent).filter(EmployeeComponent.department_id == department_id))
        return list(result.scalars().all())
