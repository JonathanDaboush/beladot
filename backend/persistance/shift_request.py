
# ------------------------------------------------------------------------------
# shift_request.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the shift_request table.
# This module defines the ShiftRequest class, which represents a request for a
# shift by an employee. Tracks shift, requesting employee, manager, and status.
# ------------------------------------------------------------------------------

from sqlalchemy import BigInteger, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from .base import Base
from .enums import PTOStatusEnum

class ShiftRequest(Base):
    """
    ORM model for the 'shift_request' table.
    Represents a request for a shift by an employee.

    Attributes:
        shift_request_id (BigInteger): Primary key for the shift request.
        shift_id (BigInteger): Foreign key referencing the shift.
        requesting_emp_id (BigInteger): Foreign key referencing the requesting employee.
        approved_by_manager_id (BigInteger): Foreign key referencing the approving manager.
        status (Enum): Status of the shift request (see PTOStatusEnum).
        # Relationships to shift, employee, and manager are defined elsewhere.
    """
    __tablename__ = 'shift_request'
    shift_request_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    shift_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('shift.shift_id'))
    requesting_emp_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('employee.emp_id'))
    approved_by_manager_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('manager.manager_id'))
    status: Mapped['PTOStatusEnum'] = mapped_column(Enum(PTOStatusEnum))
    # Relationships (to be completed in shift.py, employee.py, manager.py)
