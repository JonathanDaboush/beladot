
# ------------------------------------------------------------------------------
# employee_payment.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the employee_payment table.
# This module defines the EmployeePayment class, which represents a payment made
# to an employee. Includes payment amount, type, status, and processing details.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import BigInteger, Numeric, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .enums import PayoutStatusEnum


class EmployeePayment(Base):
    """
    ORM model for the 'employee_payment' table.
    Represents a payment made to an employee.

    Attributes:
        payment_id (BigInteger): Primary key for the payment.
        emp_id (BigInteger): Foreign key referencing the employee.
        amount (Numeric): Amount paid to the employee.
        payment_type (String): Type of payment (e.g., salary, bonus).
        status (Enum): Status of the payment (see PayoutStatusEnum).
        processed_by_finance_emp_id (BigInteger): Foreign key referencing the finance employee who processed the payment.
        created_at (DateTime): Timestamp when the payment was created.
        paid_at (DateTime): Timestamp when the payment was completed.
        # Relationships to employee and finance_employee are defined elsewhere.
    """
    __tablename__ = 'employee_payment'
    payment_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    emp_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('employee.emp_id'))
    amount: Mapped[float] = mapped_column(Numeric(10,2))
    payment_type: Mapped[str] = mapped_column(String(50))
    status: Mapped[PayoutStatusEnum] = mapped_column(Enum(PayoutStatusEnum))
    processed_by_finance_emp_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('finance_employee.finance_emp_id'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    paid_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    # Relationships (to be completed in employee.py, finance_employee.py)
