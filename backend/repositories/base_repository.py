from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')
ID = TypeVar('ID')

class BaseRepository(ABC, Generic[T, ID]):
    def __init__(self, session: AsyncSession):
        self.session = session

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
