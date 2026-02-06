
# ------------------------------------------------------------------------------
# pto_snapshot.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the pto_snapshot table.
# This module defines the PTOSnapshot class, which represents a snapshot of an
# employee's paid time off (PTO) at a specific point in time. Used for
# historical or auditing purposes.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import String, Integer, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class PTOSnapshot(Base):
    """
    ORM model for the 'pto_snapshot' table.
    Represents a snapshot of an employee's PTO for historical/auditing purposes.

    Attributes:
        employee_name (String): Full name of the employee (primary key).
        incident_number (BigInteger): Associated incident number, if any.
        pto_days (Integer): Number of PTO days taken in the period.
        created_at (DateTime): Timestamp when the snapshot was created.
    """
    __tablename__ = 'pto_snapshot'
    employee_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    incident_number: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    pto_days: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
