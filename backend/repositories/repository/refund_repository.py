"""
refund_repository.py

Repository class for managing Refund entities in the database.
Provides async methods for retrieving refunds by ID.
"""

from typing import Optional
from backend.persistance.refund import Refund
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class RefundRepository:
    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with an async database session.
        Args:
            db (AsyncSession): SQLAlchemy async session.
        """
        self.db = db

    async def get_by_id(self, refund_id: int) -> Optional[Refund]:
        """
        Retrieve a refund by its ID.
        Args:
            refund_id (int): The ID of the refund.
        Returns:
            Refund or None
        """
        result = await self.db.execute(
            select(Refund).filter(Refund.refund_id == refund_id)
        )
        return result.scalars().first()

    async def save(self, obj: Refund) -> Refund:
        """
        Save a refund entity.
        Args:
            obj (Refund): The refund to save.
        Returns:
            Refund: The saved refund.
        """
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
