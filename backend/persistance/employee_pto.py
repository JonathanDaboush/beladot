
# ------------------------------------------------------------------------------
# employee_pto.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the employee_pto table.
# This module defines the EmployeePTO class, which represents a paid time off
# (PTO) request by an employee. Includes PTO dates, status, and approval info.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, BigInteger, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
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
    pto_id = Column(BigInteger, primary_key=True)
    emp_id = Column(BigInteger, ForeignKey('employee.emp_id'))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum(PTOStatusEnum))
    approved_by_manager_id = Column(BigInteger, ForeignKey('manager.manager_id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    # Relationships (to be completed in employee.py, manager.py)
