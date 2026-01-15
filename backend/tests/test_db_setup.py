# test_db_setup.py
# Utility to create all tables for testing
from backend.persistance.base import Base, engine
import backend.persistance.employee
import backend.persistance.incident
import backend.persistance.user
import backend.persistance.department
# Import other ORM models as needed

def create_all():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_all()
    print("All tables created.")
