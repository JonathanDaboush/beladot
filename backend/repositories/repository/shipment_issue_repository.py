



"""
shipment_issue_repository.py

Repository class for managing ShipmentIssue entities in the database.
Provides async methods for retrieving and updating shipment issues by ID.
"""

from typing import Optional
from backend.persistance.shipment_issue import ShipmentIssue
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class ShipmentIssueRepository:
    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with an async database session.
        Args:
            db (AsyncSession): SQLAlchemy async session.
        """
        self.db = db

    async def get_by_id(self, issue_id: int) -> Optional[ShipmentIssue]:
        """
        Retrieve a shipment issue by its ID.
        Args:
            issue_id (int): The ID of the shipment issue.
        Returns:
            ShipmentIssue or None
        """
        result = await self.db.execute(
            select(ShipmentIssue).filter(ShipmentIssue.issue_id == issue_id)
        )
        return result.scalars().first()

    async def update(self, issue_id: int, **kwargs) -> Optional[ShipmentIssue]:
        """
        Update a shipment issue by ID.
        Args:
            issue_id (int): The ID of the shipment issue to update.
            **kwargs: Fields to update.
        Returns:
            ShipmentIssue or None: The updated issue, or None if not found.
        """
        issue = await self.get_by_id(issue_id)
        if not issue:
            return None
        for k, v in kwargs.items():
            if hasattr(issue, k):
                setattr(issue, k, v)
        await self.db.commit()
        return issue

    async def save(self, obj: ShipmentIssue) -> ShipmentIssue:
        """
        Save a shipment issue entity.
        Args:
            obj (ShipmentIssue): The shipment issue to save.
        Returns:
            ShipmentIssue: The saved shipment issue.
        """
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
