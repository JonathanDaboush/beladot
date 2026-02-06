
# ------------------------------------------------------------------------------
# product_comment_repository.py
# ------------------------------------------------------------------------------
# Repository for accessing ProductComment records from the database.
# Provides async CRUD methods for product comments and product-specific queries.
# ------------------------------------------------------------------------------

from typing import Optional, List
from backend.persistance.product_comment import ProductComment
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.repositories.base_repository import BaseRepository


class ProductCommentRepository(BaseRepository[ProductComment, int]):
    """Repository for ProductComment model implementing BaseRepository contract."""
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    UPDATABLE_FIELDS = {"comment"}

    async def get(self, id: int) -> Optional[ProductComment]:
        result = await self.session.execute(
            select(ProductComment).filter(ProductComment.comment_id == id, ProductComment.is_deleted == False)
        )
        return result.scalars().first()

    async def list(self, *, limit: int = 100, offset: int = 0) -> List[ProductComment]:
        BaseRepository.validate_pagination(limit, offset)
        result = await self.session.execute(
            select(ProductComment).filter(ProductComment.is_deleted == False).limit(limit).offset(offset)
        )
        items: List[ProductComment] = list(result.scalars().all())
        return items

    async def add(self, obj: ProductComment) -> ProductComment:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj: ProductComment) -> ProductComment:
        existing = await self.get(id)
        if not existing:
            raise ValueError(f"ProductComment with id {id} not found")
        self.apply_whitelist_update(existing, obj, self.UPDATABLE_FIELDS)
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    # Service layer compatibility
    async def get_by_id(self, id: int) -> Optional[ProductComment]:
        """Alias for get() to match service layer expectations."""
        return await self.get(id)

    async def delete(self, id: int) -> None:
        existing = await self.get(id)
        if existing:
            await self.soft_delete(existing)
        return None

    async def get_comments_for_product(self, product_id: int) -> List[ProductComment]:
        """Helper: retrieve comments for a product (keeps existing API)."""
        result = await self.session.execute(
            select(ProductComment).filter(ProductComment.product_id == product_id, ProductComment.is_deleted == False)
        )
        items: List[ProductComment] = list(result.scalars().all())
        return items
