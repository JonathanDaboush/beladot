
# ------------------------------------------------------------------------------
# paystub_snapshot.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the paystub_snapshot table.
# This module defines the PaystubSnapshot class, which represents a snapshot of
# an employee's paystub at a specific point in time. Used for historical or
# auditing purposes.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import String, Integer, Float, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class PaystubSnapshot(Base):
    """
    ORM model for the 'paystub_snapshot' table.
    Represents a snapshot of an employee's paystub for historical/auditing purposes.

    Attributes:
        employee_name (String): Full name of the employee (primary key).
        incident_number (BigInteger): Associated incident number, if any.
        hours_worked (Float): Number of hours worked in the pay period.
        sick_days (Integer): Number of sick days taken in the pay period.
        pto_days (Integer): Number of paid time off days taken in the pay period.
        hourly_rate (Float): Hourly pay rate for the employee.
        gross_pay (Float): Gross pay before deductions.
        deductions (Float): Total deductions for the pay period.
        net_pay (Float): Net pay after deductions.
        created_at (DateTime): Timestamp when the snapshot was created.
    """
    __tablename__ = 'paystub_snapshot'
    employee_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    incident_number: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    hours_worked: Mapped[float] = mapped_column(Float)
    sick_days: Mapped[int] = mapped_column(Integer)
    pto_days: Mapped[int] = mapped_column(Integer)
    hourly_rate: Mapped[float] = mapped_column(Float)
    gross_pay: Mapped[float] = mapped_column(Float)
    deductions: Mapped[float] = mapped_column(Float)
    net_pay: Mapped[float] = mapped_column(Float)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
