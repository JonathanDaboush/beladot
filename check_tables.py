import backend.persistance
from backend.db.base import Base

tables = sorted(Base.metadata.tables.keys())
print(f"Total tables: {len(tables)}\n")
print("All tables:")
for t in tables:
    print(f"  - {t}")

# Check for specific tables
required_tables = ['department', 'shift', 'address_snapshot', 'employee', 'manager']
print(f"\nChecking for required tables:")
for t in required_tables:
    status = "✓" if t in tables else "✗"
    print(f"{status} {t}")
