
# ------------------------------------------------------------------------------
# paystub_snapshot.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the paystub_snapshot table.
# This module defines the PaystubSnapshot class, which represents a snapshot of
# an employee's paystub at a specific point in time. Used for historical or
# auditing purposes.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, String, Integer, Float, BigInteger, DateTime
from .base import Base

class PaystubSnapshot(Base):
    """
    ORM model for the 'paystub_snapshot' table.
    Represents a snapshot of an employee's paystub for historical/auditing purposes.

    Attributes:
        employee_name (String): Full name of the employee (primary key).
        incident_number (BigInteger): Associated incident number, if any.
        hours_worked (Float): Number of hours worked in the pay period.
        sick_days (Integer): Number of sick days taken in the pay period.
        pto_days (Integer): Number of paid time off days taken in the pay period.
        hourly_rate (Float): Hourly pay rate for the employee.
        gross_pay (Float): Gross pay before deductions.
        deductions (Float): Total deductions for the pay period.
        net_pay (Float): Net pay after deductions.
        created_at (DateTime): Timestamp when the snapshot was created.
    """
    __tablename__ = 'paystub_snapshot'
    employee_name = Column(String(255), primary_key=True)
    incident_number = Column(BigInteger)
    hours_worked = Column(Float)
    sick_days = Column(Integer)
    pto_days = Column(Integer)
    hourly_rate = Column(Float)
    gross_pay = Column(Float)
    deductions = Column(Float)
    net_pay = Column(Float)
    created_at = Column(DateTime)
