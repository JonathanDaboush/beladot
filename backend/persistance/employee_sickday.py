
# ------------------------------------------------------------------------------
# employee_sickday.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the employee_sickday table.
# This module defines the EmployeeSickDay class, which represents a sick day
# request by an employee. Includes sick day date, status, and approval info.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import BigInteger, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from .base import Base
from .enums import PTOStatusEnum


class EmployeeSickDay(Base):
    """
    ORM model for the 'employee_sickday' table.
    Represents a sick day request by an employee.

    Attributes:
        sickday_id (BigInteger): Primary key for the sick day request.
        emp_id (BigInteger): Foreign key referencing the employee.
        date (Date): Date of the sick day.
        status (Enum): Status of the sick day request (see PTOStatusEnum).
        approved_by_manager_id (BigInteger): Foreign key referencing the approving manager.
        created_at (DateTime): Timestamp when the sick day request was created.
        updated_at (DateTime): Timestamp when the sick day request was last updated.
        # Relationships to employee and manager are defined elsewhere.
    """
    __tablename__ = 'employee_sickday'
    sickday_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    emp_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('employee.emp_id'))
    date: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    status: Mapped[PTOStatusEnum] = mapped_column(Enum(PTOStatusEnum))
    approved_by_manager_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('manager.manager_id'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    # Relationships (to be completed in employee.py, manager.py)

    def to_dict(self):
        """Convert sick day object to dictionary."""
        return {
            'sickday_id': self.sickday_id,
            'emp_id': self.emp_id,
            'date': self.date.isoformat() if self.date else None,
            'status': self.status.value if hasattr(self.status, 'value') else str(self.status),
            'approved_by_manager_id': self.approved_by_manager_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
