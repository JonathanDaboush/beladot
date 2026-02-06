# test_db_setup.py
# Utility to create all tables for testing
from backend.persistance.base import Base
from backend.persistance.base import Base, get_engine

def create_all():
    Base.metadata.create_all(bind=get_engine())

if __name__ == "__main__":
    create_all()
    print("All tables created.")
