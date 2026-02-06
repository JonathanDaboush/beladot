"""
sickday_snapshot.py

SQLAlchemy ORM model for the sickday_snapshot table.
Represents a snapshot of an employee's sick days for a given period.
"""


from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import String, Integer, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class SickDaySnapshot(Base):
    __tablename__ = 'sickday_snapshot'
    employee_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    incident_number: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    sick_days: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
