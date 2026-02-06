
# ------------------------------------------------------------------------------
# finance_employee.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the finance_employee table.
# This module defines the FinanceEmployee class, which represents an employee
# with finance-related responsibilities. Tracks activity and links to employee
# and payment records.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from .base import Base


class FinanceEmployee(Base):
    """
    ORM model for the 'finance_employee' table.
    Represents an employee with finance responsibilities.

    Attributes:
        finance_emp_id (BigInteger): Primary key for the finance employee.
        emp_id (BigInteger): Foreign key referencing the employee.
        is_active (Boolean): Whether the finance employee is currently active.
        created_at (DateTime): Timestamp when the finance employee record was created.
        last_active_at (DateTime): Timestamp when the finance employee was last active.
        # Relationships to employee and employee_payment are defined elsewhere.
    """
    __tablename__ = 'finance_employee'
    finance_emp_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    emp_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('employee.emp_id'))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    last_active_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    # Relationships (to be completed in employee.py, employee_payment.py)
