"""
user_snapshot.py

SQLAlchemy ORM model for the user_snapshot table.
Represents a snapshot of user information, including contact and account details.
"""


from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from backend.db.base import Base

class UserSnapshot(Base):
    __tablename__ = 'user_snapshot'
    full_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    account_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    bank: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    approved_by_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
