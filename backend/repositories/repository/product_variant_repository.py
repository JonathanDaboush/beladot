
# ------------------------------------------------------------------------------
# product_variant_repository.py
# ------------------------------------------------------------------------------
# Repository for accessing ProductVariant records from the database.
# Provides async CRUD methods and stock management for product variants.
# ------------------------------------------------------------------------------

from typing import Optional
from backend.persistance.product_variant import ProductVariant
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class ProductVariantRepository:
    """
    Repository for ProductVariant model.
    Provides async CRUD operations and stock management for product variants.
    """
    def __init__(self, db: AsyncSession):
        """Initialize repository with async DB session."""
        self.db = db

    async def decrement_stock(self, variant_id: int, qty: int) -> bool:
        """Decrement the quantity of a product variant by a given amount if sufficient quantity exists."""
        result = await self.db.execute(
            select(ProductVariant).filter(ProductVariant.variant_id == variant_id, ProductVariant.quantity >= qty, ProductVariant.is_active == True)
        )
        variant = result.scalars().first()
        if variant:
            variant.quantity -= qty
            await self.db.commit()
            return True
        return False

    async def get_by_id(self, variant_id: int) -> Optional[ProductVariant]:
        """Retrieve a product variant by its ID, restricted to active variants."""
        result = await self.db.execute(
            select(ProductVariant).filter(ProductVariant.variant_id == variant_id, ProductVariant.is_active == True)
        )
        return result.scalars().first()

    async def save(self, variant: ProductVariant) -> ProductVariant:
        """Save a new product variant to the database."""
        self.db.add(variant)
        await self.db.commit()
        await self.db.refresh(variant)
        return variant

    async def update(self, variant_id: int, **kwargs) -> Optional[ProductVariant]:
        """Update an existing product variant by ID with provided fields."""
        variant = await self.get_by_id(variant_id)
        if not variant:
            return None
        for k, v in kwargs.items():
            if hasattr(variant, k):
                setattr(variant, k, v)
        await self.db.commit()
        return variant

    async def delete(self, variant_id: int) -> bool:
        """Soft delete a product variant by its ID (marks as inactive)."""
        variant = await self.get_by_id(variant_id)
        if variant:
            variant.is_active = False
            await self.db.commit()
            return True
        return False
