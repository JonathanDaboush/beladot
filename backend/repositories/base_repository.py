from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')
ID = TypeVar('ID')

class BaseRepository(ABC, Generic[T, ID]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def soft_delete(self, obj: T) -> None:
        """Perform a soft-delete if the model has `is_deleted`, otherwise hard-delete."""
        if hasattr(obj, "is_deleted"):
            setattr(obj, "is_deleted", True)
            await self.session.commit()
            return
        if hasattr(obj, "deleted"):
            setattr(obj, "deleted", True)
            await self.session.commit()
            return
        # Fallback to hard delete when model doesn't have a soft-delete column
        await self.session.delete(obj)
        await self.session.commit()

    def apply_whitelist_update(self, target: T, source: T, whitelist: set[str]) -> None:
        """Copy only whitelisted attributes from source to target."""
        for field in whitelist:
            if hasattr(source, field) and hasattr(target, field):
                setattr(target, field, getattr(source, field))

    # Defensive pagination guard
    @staticmethod
    def validate_pagination(limit: int = 100, offset: int = 0) -> None:
        if limit <= 0:
            raise ValueError("limit must be > 0")
        if limit > 1000:
            raise ValueError("limit must be <= 1000")
        if offset < 0:
            raise ValueError("offset must be >= 0")

    @abstractmethod
    async def get(self, id: ID) -> Optional[T]:
        pass

    @abstractmethod
    async def list(self, *, limit: int = 100, offset: int = 0) -> List[T]:
        pass

    @abstractmethod
    async def add(self, obj: T) -> T:
        pass

    @abstractmethod
    async def update(self, id: ID, obj: T) -> T:
        pass

    @abstractmethod
    async def delete(self, id: ID) -> None:
        pass
