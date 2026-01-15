
# ------------------------------------------------------------------------------
# shift.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the shift table.
# This module defines the Shift class, which represents a work shift assigned to
# an employee. Tracks department, assigned employee, times, manager, and status.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, BigInteger, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .enums import ShiftStatusEnum

class Shift(Base):
    """
    ORM model for the 'shift' table.
    Represents a work shift assigned to an employee.

    Attributes:
        shift_id (BigInteger): Primary key for the shift.
        department_id (BigInteger): Foreign key referencing the department.
        assigned_emp_id (BigInteger): Foreign key referencing the assigned employee.
        start_time (DateTime): Start time of the shift.
        end_time (DateTime): End time of the shift.
        created_by_manager_id (BigInteger): Foreign key referencing the manager who created the shift.
        status (Enum): Status of the shift (see ShiftStatusEnum).
        # Relationships to department, employee, manager, and shift_request are defined elsewhere.
    """
    __tablename__ = 'shift'
    from sqlalchemy import Integer
    shift_id = Column(Integer, primary_key=True, autoincrement=True)
    department_id = Column(BigInteger, ForeignKey('department.department_id'))
    assigned_emp_id = Column(BigInteger, ForeignKey('employee.emp_id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    created_by_manager_id = Column(BigInteger, ForeignKey('manager.manager_id'))
    status = Column(Enum(ShiftStatusEnum))
    # Relationships (to be completed in department.py, employee.py, manager.py, shift_request.py)
