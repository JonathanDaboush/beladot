
# ------------------------------------------------------------------------------
# incident.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the incident table.
# This module defines the Incident class, which represents an incident involving
# an employee. Tracks description, cost, date, and status flags.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, Integer, BigInteger, String, Float, Boolean, ForeignKey
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
    incident_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(BigInteger, ForeignKey('employee.emp_id'))
    description = Column(String(255))
    cost = Column(Float)
    date = Column(String(32))  # ISO date string for simplicity
    status = Column(String(32), default='open')
    status_addressed = Column(Boolean, default=False)
    paid_all = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)
