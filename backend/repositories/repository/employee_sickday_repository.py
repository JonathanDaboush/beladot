
# ------------------------------------------------------------------------------
# employee_sickday_repository.py
# ------------------------------------------------------------------------------
# Repository for accessing EmployeeSickDay records from the database.
# Provides methods for retrieving employee sick days by ID.
# ------------------------------------------------------------------------------

from typing import Optional, List
from backend.persistance.employee_sickday import EmployeeSickDay
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class EmployeeSickDayRepository:
    """
    Repository for EmployeeSickDay model.
    Provides methods to retrieve employee sick days by ID.
    """
    def __init__(self, db: AsyncSession):
        """Initialize repository with DB session."""
        self.db = db

    async def get_by_id(self, sickday_id: int) -> Optional[EmployeeSickDay]:
        """Retrieve an employee sick day record by its ID."""
        result = await self.db.execute(
            select(EmployeeSickDay).filter(EmployeeSickDay.sickday_id == sickday_id)
        )
        return result.scalars().first()

    async def get_by_employee_id(self, emp_id: int, start_date=None, end_date=None) -> List[EmployeeSickDay]:
        """Get sick day records for an employee, optionally filtered by date range."""
        stmt = select(EmployeeSickDay).filter(EmployeeSickDay.emp_id == emp_id)
        if start_date:
            stmt = stmt.filter(EmployeeSickDay.date >= start_date)
        if end_date:
            stmt = stmt.filter(EmployeeSickDay.date <= end_date)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def save(self, sickday: EmployeeSickDay) -> EmployeeSickDay:
        """Save a sick day record."""
        self.db.add(sickday)
        await self.db.commit()
        await self.db.refresh(sickday)
        return sickday

    async def update(self, sickday_id: int, **kwargs) -> Optional[EmployeeSickDay]:
        """Update a sick day record."""
        sickday = await self.get_by_id(sickday_id)
        if not sickday:
            return None
        for key, value in kwargs.items():
            if hasattr(sickday, key):
                setattr(sickday, key, value)
        await self.db.commit()
        await self.db.refresh(sickday)
        return sickday

    async def delete(self, sickday_id: int) -> bool:
        """Delete a sick day record."""
        sickday = await self.get_by_id(sickday_id)
        if not sickday:
            return False
        await self.db.delete(sickday)
        await self.db.commit()
        return True
