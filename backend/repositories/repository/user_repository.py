"""
user_repository.py

Repository class for managing User entities in the database.
Provides async CRUD operations and password management for users.
"""

from typing import Optional, List
from backend.persistance.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User, int]):
    def __init__(self, db: AsyncSession):
        """Initialize repository and store session on `self.session`."""
        super().__init__(db)

    async def get(self, id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.
        Args:
            user_id (int): The ID of the user.
        Returns:
            User or None
        """
        result = await self.session.execute(select(User).where(User.user_id == id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.
        Args:
            email (str): The email address of the user.
        Returns:
            User or None
        """
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    async def list(self, *, limit: int = 100, offset: int = 0) -> List[User]:
        """
        List users with pagination and deterministic ordering.
        Args:
            limit (int): Max number of users to return.
            offset (int): Number of users to skip.
        Returns:
            List[User]
        """
        result = await self.session.execute(
            select(User).order_by(User.user_id).limit(limit).offset(offset)
        )
        items: List[User] = list(result.scalars().all())
        return items

    async def add(self, obj: User) -> User:
        """
        Add a new user to the database.
        Args:
            user (User): The user to add.
        Returns:
            User: The added user.
        """
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj: User) -> User:
        """
        Update an existing user in the database.
        Args:
            user (User): The user to update.
        Returns:
            User: The updated user.
        """
        merged = await self.session.merge(obj)
        await self.session.flush()
        return merged

    async def update_password_by_email(self, email: str, new_password: str) -> bool:
        """
        Update a user's password by their email address.
        Args:
            email (str): The email address of the user.
            new_password (str): The new password to set.
        Returns:
            bool: True if updated, False otherwise.
        """
        user = await self.get_by_email(email)
        if user:
            user.password = new_password
            await self.update(user.user_id, user)
            return True
        return False

    async def delete(self, id: int) -> None:
        """
        Remove a user from the database by their ID.
        Args:
            user_id (int): The ID of the user to remove.
        Returns:
            User or None: The removed user, or None if not found.
        """
        user = await self.get(id)
        if user:
            await self.soft_delete(user)
        return None
    async def remove_user(self, user: User) -> None:
        """Remove a user instance from the DB (non-interface helper)."""
        await self.soft_delete(user)
        return None
