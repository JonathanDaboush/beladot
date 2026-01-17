
# ------------------------------------------------------------------------------
# product_repository.py
# ------------------------------------------------------------------------------
# Repository for accessing Product records from the database.
# Provides async CRUD methods and stock management for products.
# ------------------------------------------------------------------------------

from backend.persistance.product import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class ProductRepository:
    """
    Repository for Product model.
    Provides async CRUD operations and stock management for products.
    """
    def __init__(self, db: AsyncSession):
        """Initialize repository with async DB session."""
        self.db = db

    async def decrement_stock(self, product_id, qty):
        """Decrement product availability when purchasing a non-variant product.
        The Product model does not track stock; treat as available if active.
        """
        result = await self.db.execute(
            select(Product).filter(Product.product_id == product_id, Product.is_active == True)
        )
        product = result.scalars().first()
        if product:
            # No stock field on Product; assume purchase allowed when active.
            await self.db.commit()
            return True
        return False

    async def get_by_id(self, product_id):
        """Retrieve a product by its ID, restricted to active products."""
        result = await self.db.execute(
            select(Product).filter(Product.product_id == product_id, Product.is_active == True)
        )
        return result.scalars().first()

    async def save(self, product):
        """Save a new product to the database."""
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def update(self, product_id, **kwargs):
        """Update an existing product by ID with provided fields."""
        product = await self.get_by_id(product_id)
        if not product:
            return None
        for k, v in kwargs.items():
            if hasattr(product, k):
                setattr(product, k, v)
        await self.db.commit()
        return product

    async def delete(self, product_id):
        """Soft delete a product by its ID (marks as inactive)."""
        product = await self.get_by_id(product_id)
        if product:
            product.is_active = False
            await self.db.commit()
            return True
        return False
