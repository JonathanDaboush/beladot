
# ------------------------------------------------------------------------------
# reimbursement_snapshot.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the reimbursement_snapshot table.
# This module defines the ReimbursementSnapshot class, which represents a
# snapshot of a reimbursement at a specific point in time. Used for historical
# or auditing purposes.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import String, Float, BigInteger, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class ReimbursementSnapshot(Base):
    """
    ORM model for the 'reimbursement_snapshot' table.
    Represents a snapshot of a reimbursement for historical/auditing purposes.

    Attributes:
        employee_name (String): Full name of the employee (primary key).
        incident_number (BigInteger): Associated incident number, if any.
        amount (Float): Amount reimbursed.
        description (Text): Description of the reimbursement.
        created_at (DateTime): Timestamp when the snapshot was created.
    """
    __tablename__ = 'reimbursement_snapshot'
    employee_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    incident_number: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
