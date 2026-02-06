
# ------------------------------------------------------------------------------
# product_variant_image_repository.py
# ------------------------------------------------------------------------------
# Repository for accessing ProductVariantImage records from the database.
# Provides async CRUD methods for product variant images and variant-specific queries.
# ------------------------------------------------------------------------------

from typing import Optional, List
from backend.persistance.product_variant_image import ProductVariantImage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.repositories.base_repository import BaseRepository


class ProductVariantImageRepository(BaseRepository[ProductVariantImage, int]):
    """Repository for ProductVariantImage implementing BaseRepository contract."""
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    UPDATABLE_FIELDS = {"image_url", "variant_id"}

    async def get(self, id: int) -> Optional[ProductVariantImage]:
        result = await self.session.execute(
            select(ProductVariantImage).filter(ProductVariantImage.image_id == id)
        )
        return result.scalars().first()

    async def list(self, *, limit: int = 100, offset: int = 0) -> List[ProductVariantImage]:
        BaseRepository.validate_pagination(limit, offset)
        result = await self.session.execute(select(ProductVariantImage).limit(limit).offset(offset))
        items: List[ProductVariantImage] = list(result.scalars().all())
        return items

    async def add(self, obj: ProductVariantImage) -> ProductVariantImage:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj: ProductVariantImage) -> ProductVariantImage:
        existing = await self.get(id)
        if not existing:
            raise ValueError(f"ProductVariantImage with id {id} not found")
        self.apply_whitelist_update(existing, obj, self.UPDATABLE_FIELDS)
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def delete(self, id: int) -> None:
        existing = await self.get(id)
        if existing:
            await self.soft_delete(existing)
        return None

    async def get_by_variant_id(self, variant_id: int) -> List[ProductVariantImage]:
        result = await self.session.execute(
            select(ProductVariantImage).filter(ProductVariantImage.variant_id == variant_id)
        )
        return list(result.scalars().all())

    # Service layer compatibility
    async def save(self, obj: ProductVariantImage) -> ProductVariantImage:
        """Alias for add() to match service layer expectations."""
        return await self.add(obj)
        items: List[ProductVariantImage] = list(result.scalars().all())
        return items
