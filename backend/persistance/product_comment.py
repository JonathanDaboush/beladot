
# ------------------------------------------------------------------------------
# product_comment.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the product_comment table.
# Represents a user's comment on a product with soft-delete support.
# ------------------------------------------------------------------------------


from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import BigInteger, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from backend.db.base import Base

class ProductComment(Base):
    __tablename__ = 'product_comment'
    comment_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('product.product_id'), nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    comment: Mapped[str] = mapped_column(String(1000), nullable=False)
    response: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
