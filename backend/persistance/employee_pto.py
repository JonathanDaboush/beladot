
# ------------------------------------------------------------------------------
# employee_pto.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the employee_pto table.
# This module defines the EmployeePTO class, which represents a paid time off
# (PTO) request by an employee. Includes PTO dates, status, and approval info.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import BigInteger, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .enums import PTOStatusEnum


class EmployeePTO(Base):
    """
    ORM model for the 'employee_pto' table.
    Represents a paid time off (PTO) request by an employee.

    Attributes:
        pto_id (BigInteger): Primary key for the PTO request.
        emp_id (BigInteger): Foreign key referencing the employee.
        start_date (Date): Start date of the PTO.
        end_date (Date): End date of the PTO.
        status (Enum): Status of the PTO request (see PTOStatusEnum).
        approved_by_manager_id (BigInteger): Foreign key referencing the approving manager.
        created_at (DateTime): Timestamp when the PTO request was created.
        updated_at (DateTime): Timestamp when the PTO request was last updated.
        # Relationships to employee and manager are defined elsewhere.
    """
    __tablename__ = 'employee_pto'
    pto_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    emp_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('employee.emp_id'))
    start_date: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    status: Mapped[PTOStatusEnum] = mapped_column(Enum(PTOStatusEnum))
    approved_by_manager_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('manager.manager_id'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    # Relationships (to be completed in employee.py, manager.py)

    def to_dict(self):
        """Convert PTO object to dictionary."""
        return {
            'pto_id': self.pto_id,
            'emp_id': self.emp_id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status.value if hasattr(self.status, 'value') else str(self.status),
            'approved_by_manager_id': self.approved_by_manager_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
