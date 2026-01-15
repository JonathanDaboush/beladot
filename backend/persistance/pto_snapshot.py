
# ------------------------------------------------------------------------------
# pto_snapshot.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the pto_snapshot table.
# This module defines the PTOSnapshot class, which represents a snapshot of an
# employee's paid time off (PTO) at a specific point in time. Used for
# historical or auditing purposes.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, String, Integer, BigInteger, DateTime
from .base import Base

class PTOSnapshot(Base):
    """
    ORM model for the 'pto_snapshot' table.
    Represents a snapshot of an employee's PTO for historical/auditing purposes.

    Attributes:
        employee_name (String): Full name of the employee (primary key).
        incident_number (BigInteger): Associated incident number, if any.
        pto_days (Integer): Number of PTO days taken in the period.
        created_at (DateTime): Timestamp when the snapshot was created.
    """
    __tablename__ = 'pto_snapshot'
    employee_name = Column(String(255), primary_key=True)
    incident_number = Column(BigInteger)
    pto_days = Column(Integer)
    created_at = Column(DateTime)
