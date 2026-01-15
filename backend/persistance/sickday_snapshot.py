"""
sickday_snapshot.py

SQLAlchemy ORM model for the sickday_snapshot table.
Represents a snapshot of an employee's sick days for a given period.
"""

from sqlalchemy import Column, String, Integer, DateTime, BigInteger
from .base import Base

class SickDaySnapshot(Base):
    __tablename__ = 'sickday_snapshot'
    employee_name = Column(String(255), primary_key=True)
    incident_number = Column(BigInteger)
    sick_days = Column(Integer)
    created_at = Column(DateTime)
