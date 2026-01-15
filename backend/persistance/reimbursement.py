
# ------------------------------------------------------------------------------
# reimbursement.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the reimbursement table.
# This module defines the Reimbursement class, which represents a reimbursement
# record for an incident. Tracks incident, description, response, amount, and status flags.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, BigInteger, String, Float, Boolean, ForeignKey
from .base import Base

class Reimbursement(Base):
    """
    ORM model for the 'reimbursement' table.
    Represents a reimbursement record for an incident.

    Attributes:
        reimbursement_id (BigInteger): Primary key for the reimbursement.
        incident_id (BigInteger): Foreign key referencing the incident.
        description (String): Description of the reimbursement request.
        response (String): Response to the reimbursement request (optional).
        amount_approved (Float): Amount approved for reimbursement (optional).
        status (Boolean): Status of the reimbursement (e.g., processed or not).
        status_addressed (Boolean): Whether the reimbursement has been addressed.
        paid_all (Boolean): Whether the full amount has been paid.
        deleted (Boolean): Whether the reimbursement record is deleted (soft delete).
    """
    __tablename__ = 'reimbursement'
    reimbursement_id = Column(BigInteger, primary_key=True)
    # employee_id removed, now on Incident
    incident_id = Column(BigInteger, ForeignKey('incident.incident_id'))
    description = Column(String(255))
    response = Column(String(255), nullable=True)
    amount_approved = Column(Float, nullable=True)
    status = Column(Boolean, default=False)
    status_addressed = Column(Boolean, default=False)
    paid_all = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)
