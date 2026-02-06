
# ------------------------------------------------------------------------------
# shift.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the shift table.
# This module defines the Shift class, which represents a work shift assigned to
# an employee. Tracks department, assigned employee, times, manager, and status.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
import datetime

from sqlalchemy import Integer, BigInteger, DateTime, Enum, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import ShiftStatusEnum


class Shift(Base):
    def to_dict(self):
        return {
            'shift_id': getattr(self, 'shift_id', None),
            'start_time': getattr(self, 'start_time', None),
            'end_time': getattr(self, 'end_time', None),
            'emp_id': getattr(self, 'emp_id', None),
        }
    """
    ORM model for the 'shift' table.
    Represents a work shift assigned to an employee.
    """
    __tablename__ = 'shift'

    shift_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    emp_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('employee.emp_id'))
    start_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    end_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_by_manager_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('manager.manager_id'))
    status: Mapped['ShiftStatusEnum'] = mapped_column(Enum(ShiftStatusEnum))
    # Relationships (to be completed in department.py, employee.py, manager.py, shift_request.py)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
