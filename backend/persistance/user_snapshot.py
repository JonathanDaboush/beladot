"""
user_snapshot.py

SQLAlchemy ORM model for the user_snapshot table.
Represents a snapshot of user information, including contact and account details.
"""

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserSnapshot(Base):
    __tablename__ = 'user_snapshot'
    full_name = Column(String(255), primary_key=True)
    email = Column(String(255))
    phone_number = Column(String(20))
    account_type = Column(String(50))
    bank = Column(String(100))
    approved_by_name = Column(String(255))
