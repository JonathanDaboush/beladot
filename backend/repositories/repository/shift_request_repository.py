


"""
shift_request_repository.py

Repository class for managing ShiftRequest entities in the database.
Provides async method for retrieving shift requests by ID.
"""

from typing import Optional
from backend.persistance.shift_request import ShiftRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class ShiftRequestRepository:
    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with an async database session.
        Args:
            db (AsyncSession): SQLAlchemy async session.
        """
        self.db = db

    async def get_by_id(self, shift_request_id: int) -> Optional[ShiftRequest]:
        """
        Retrieve a shift request by its ID.
        Args:
            shift_request_id (int): The ID of the shift request.
        Returns:
            Optional[ShiftRequest]
        """
        result = await self.db.execute(
            select(ShiftRequest).filter(ShiftRequest.shift_request_id == shift_request_id)
        )
        return result.scalars().first()
