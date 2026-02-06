
# ------------------------------------------------------------------------------
# order_repository.py
# ------------------------------------------------------------------------------
# Repository for accessing Order records from the database.
# Provides async CRUD and filtering methods for orders, including advanced filters.
# ------------------------------------------------------------------------------

from typing import Optional, List
from datetime import date
from backend.persistance.order import Order
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.repositories.base_repository import BaseRepository


class OrderRepository(BaseRepository[Order, int]):
    """
    Repository for Order model.
    Provides async CRUD operations and advanced filtering for orders.
    """
    def __init__(self, session: AsyncSession):
        """Initialize repository with async DB session."""
        super().__init__(session)

    # Whitelist of fields that are safe to update via `update()`.
    UPDATABLE_FIELDS = {"order_status", "total_amount", "cart_id", "updated_at"}

    async def filter_orders(self, product_id: Optional[int] = None, age_range: Optional[tuple[int, int]] = None, sex: Optional[str] = None, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Order]:
        """
        Retrieve orders filtered by product, user age range, sex, and date range.
        Args:
            product_id (int, optional): Filter by product ID.
            age_range (tuple, optional): (min_age, max_age) to filter users by age.
            sex (str, optional): Filter users by sex.
            start_date (date, optional): Filter orders created after this date.
            end_date (date, optional): Filter orders created before this date.
        Returns:
            list[Order]: List of filtered Order objects.
        """
        stmt = select(Order).filter(Order.is_deleted == False)
        if start_date:
            stmt = stmt.filter(Order.created_at >= start_date)
        if end_date:
            stmt = stmt.filter(Order.created_at <= end_date)
        if product_id:
            from backend.persistance.order_item import OrderItem
            # Use a JOIN to filter orders that have an OrderItem with the given product_id.
            stmt = stmt.join(OrderItem, Order.order_id == OrderItem.order_id).filter(OrderItem.product_id == product_id)
        if age_range or sex:
            from backend.persistance.user import User
            stmt = stmt.join(User, Order.user_id == User.user_id)
            if age_range:
                import datetime
                today = datetime.date.today()
                min_age: int
                max_age: int
                min_age, max_age = age_range
                min_dob = today.replace(year=today.year - max_age)
                max_dob = today.replace(year=today.year - min_age)
                stmt = stmt.filter(User.dob >= min_dob, User.dob <= max_dob)
            if sex:
                # Defensive: Only filter if User model has 'sex' attribute
                if hasattr(User, 'sex'):
                    stmt = stmt.filter(getattr(User, 'sex') == sex)
        result = await self.session.execute(stmt)
        items: List[Order] = list(result.scalars().all())
        return items

    async def get(self, id: int) -> Optional[Order]:
        """Retrieve an order by its ID, excluding deleted orders."""
        result = await self.session.execute(
            select(Order).filter(Order.order_id == id, Order.is_deleted == False)
        )
        return result.scalars().first()

    async def list(self, *, limit: int = 100, offset: int = 0) -> List[Order]:
        BaseRepository.validate_pagination(limit, offset)
        result = await self.session.execute(
            select(Order).filter(Order.is_deleted == False).limit(limit).offset(offset)
        )
        items: List[Order] = list(result.scalars().all())
        return items

    async def add(self, obj: Order) -> Order:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj: Order) -> Order:
        existing = await self.get(id)
        if not existing:
            raise ValueError(f"Order with id {id} not found")
        # Only copy a small, explicit set of safe fields. This prevents accidental
        # overwrites of PKs, FKs, audit fields, or relationships.
        for field in self.UPDATABLE_FIELDS:
            if hasattr(obj, field):
                setattr(existing, field, getattr(obj, field))
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def delete(self, id: int) -> None:
        existing = await self.get(id)
        if existing:
            # Enforce soft-delete consistently via BaseRepository helper.
            await self.soft_delete(existing)
        return None
