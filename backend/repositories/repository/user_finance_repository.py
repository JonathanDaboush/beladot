





"""
user_finance_repository.py

Repository class for managing UserFinance entities in the database.
Provides async CRUD operations for user finance records.
"""

from typing import Optional
from backend.persistance.user_finance import UserFinance
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class UserFinanceRepository:
    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with an async database session.
        Args:
            db (AsyncSession): SQLAlchemy async session.
        """
        self.db = db

    async def get_by_id(self, uf_id: int) -> Optional[UserFinance]:
        """
        Retrieve a user finance record by its ID, excluding soft-deleted.
        Args:
            uf_id (int): The ID of the user finance record.
        Returns:
            UserFinance or None
        """
        result = await self.db.execute(
            select(UserFinance).filter(UserFinance.uf_id == uf_id, UserFinance.is_deleted == False)
        )
        return result.scalars().first()

    async def save(self, user_finance: UserFinance) -> UserFinance:
        """
        Save a new user finance record to the database.
        Args:
            user_finance (UserFinance): The user finance record to save.
        Returns:
            UserFinance: The saved user finance record.
        """
        self.db.add(user_finance)
        await self.db.commit()
        await self.db.refresh(user_finance)
        return user_finance

    async def update(self, uf_id: int, **kwargs) -> Optional[UserFinance]:
        """
        Update a user finance record by ID.
        Args:
            uf_id (int): The ID of the user finance record to update.
            **kwargs: Fields to update.
        Returns:
            UserFinance or None: The updated record, or None if not found.
        """
        user_finance = await self.get_by_id(uf_id)
        if not user_finance:
            return None
        for k, v in kwargs.items():
            if hasattr(user_finance, k):
                setattr(user_finance, k, v)
        await self.db.commit()
        return user_finance

    async def delete(self, uf_id: int) -> bool:
        """
        Soft-delete a user finance record by ID.
        Args:
            uf_id (int): The ID of the user finance record to delete.
        Returns:
            bool: True if deleted, False otherwise.
        """
        user_finance = await self.get_by_id(uf_id)
        if user_finance:
            user_finance.is_deleted = True
            await self.db.commit()
            return True
        return False
        if user_finance:
            await self.db.delete(user_finance)
            await self.db.commit()
            return True
        return False
