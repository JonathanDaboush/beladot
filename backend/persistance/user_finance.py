"""
user_finance.py

SQLAlchemy ORM model for the user_finance table.
Represents a user's financial information, including bank, card, and account type.
"""


from typing import Optional
from sqlalchemy import BigInteger, String, ForeignKey, Enum
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .enums import AccountTypeEnum

class UserFinance(Base):
    __tablename__ = 'user_finance'
    uf_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'))
    bank: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    pin: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)
    cvv: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    credit_card_number: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    account_type: Mapped[Optional[AccountTypeEnum]] = mapped_column(Enum(AccountTypeEnum), nullable=True)
    # Relationship (to be completed in user.py)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
