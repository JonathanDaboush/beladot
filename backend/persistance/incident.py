
# ------------------------------------------------------------------------------
# incident.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the incident table.
# This module defines the Incident class, which represents an incident involving
# an employee. Tracks description, cost, date, and status flags.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, BigInteger, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Incident(Base):
    """
    ORM model for the 'incident' table.
    Represents an incident involving an employee.

    Attributes:
        incident_id (BigInteger): Primary key for the incident.
        employee_id (BigInteger): Foreign key referencing the employee involved.
        description (String): Description of the incident.
        cost (Float): Cost associated with the incident.
        date (String): ISO date string representing when the incident occurred.
        status_addressed (Boolean): Whether the incident has been addressed.
        paid_all (Boolean): Whether all costs have been paid.
        deleted (Boolean): Whether the incident record is deleted (soft delete).
    """
    __tablename__ = 'incident'
    incident_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('employee.emp_id'))
    description: Mapped[str] = mapped_column(String(255))
    cost: Mapped[float] = mapped_column(Float)
    date: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)  # ISO date string for simplicity
    status: Mapped[str] = mapped_column(String(32), default='open')
    status_addressed: Mapped[bool] = mapped_column(Boolean, default=False)
    paid_all: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
