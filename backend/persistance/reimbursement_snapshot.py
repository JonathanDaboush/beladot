
# ------------------------------------------------------------------------------
# reimbursement_snapshot.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the reimbursement_snapshot table.
# This module defines the ReimbursementSnapshot class, which represents a
# snapshot of a reimbursement at a specific point in time. Used for historical
# or auditing purposes.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, String, Float, BigInteger, DateTime, Text
from .base import Base

class ReimbursementSnapshot(Base):
    """
    ORM model for the 'reimbursement_snapshot' table.
    Represents a snapshot of a reimbursement for historical/auditing purposes.

    Attributes:
        employee_name (String): Full name of the employee (primary key).
        incident_number (BigInteger): Associated incident number, if any.
        amount (Float): Amount reimbursed.
        description (Text): Description of the reimbursement.
        created_at (DateTime): Timestamp when the snapshot was created.
    """
    __tablename__ = 'reimbursement_snapshot'
    employee_name = Column(String(255), primary_key=True)
    incident_number = Column(BigInteger)
    amount = Column(Float)
    description = Column(Text)
    created_at = Column(DateTime)
