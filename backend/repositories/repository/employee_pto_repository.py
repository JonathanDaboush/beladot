
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

# ------------------------------------------------------------------------------
# employee_pto_repository.py
# ------------------------------------------------------------------------------
# Repository for accessing EmployeePTO records from the database.
# Provides methods for retrieving employee PTO by ID.
# ------------------------------------------------------------------------------

from backend.persistance.employee_pto import EmployeePTO
from sqlalchemy import select

class EmployeePTORepository:
    """
    Repository for EmployeePTO model.
    Provides methods to retrieve employee PTO by ID.
    """
    def __init__(self, db: AsyncSession):
        """Initialize repository with DB session."""
        self.db = db

    async def get_by_id(self, pto_id: int) -> Optional[EmployeePTO]:
        """Retrieve an employee PTO record by its ID."""
        result = await self.db.execute(
            select(EmployeePTO).filter(EmployeePTO.pto_id == pto_id)
        )
        return result.scalars().first()

    async def get_by_employee_id(self, emp_id: int, start_date=None, end_date=None) -> List[EmployeePTO]:
        """Get PTO records for an employee, optionally filtered by date range."""
        stmt = select(EmployeePTO).filter(EmployeePTO.employee_id == emp_id)
        if start_date:
            stmt = stmt.filter(EmployeePTO.start_date >= start_date)
        if end_date:
            stmt = stmt.filter(EmployeePTO.end_date <= end_date)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def save(self, pto: EmployeePTO) -> EmployeePTO:
        """Save a PTO record."""
        self.db.add(pto)
        await self.db.commit()
        await self.db.refresh(pto)
        return pto

    async def update(self, pto_id: int, **kwargs) -> Optional[EmployeePTO]:
        """Update a PTO record."""
        pto = await self.get_by_id(pto_id)
        if not pto:
            return None
        for key, value in kwargs.items():
            if hasattr(pto, key):
                setattr(pto, key, value)
        await self.db.commit()
        await self.db.refresh(pto)
        return pto

    async def delete(self, pto_id: int) -> bool:
        """Delete a PTO record."""
        pto = await self.get_by_id(pto_id)
        if not pto:
            return False
        await self.db.delete(pto)
        await self.db.commit()
        return True
