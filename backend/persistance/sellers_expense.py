
# ------------------------------------------------------------------------------
# sellers_expense.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the sellers_expense table.
# Represents an expense record associated with an order; amount can be
# negative (owed) or positive (given).
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
from sqlalchemy import BigInteger, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class SellerExpense(Base):
    """
    ORM model for the 'sellers_expense' table.

    Attributes:
        id (BigInteger): Primary key for the expense record.
        order_id (BigInteger): Foreign key referencing the order.
        amount (Numeric): Expense amount; negative for owed, positive for given.
    """
    __tablename__ = 'sellers_expense'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('order.order_id'), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
