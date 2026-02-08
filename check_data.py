import asyncio
from backend.persistance.async_base import AsyncSessionLocal
from backend.persistance.user import User
from backend.persistance.employee import Employee
from backend.persistance.manager import Manager
from sqlalchemy import select, func

async def main():
    async with AsyncSessionLocal() as session:
        user_count = (await session.execute(select(func.count(User.user_id)))).scalar()
        emp_count = (await session.execute(select(func.count(Employee.emp_id)))).scalar()
        mgr_count = (await session.execute(select(func.count(Manager.manager_id)))).scalar()
        
        print(f"\n📊 Seeded Data Summary:")
        print(f"  Users (customers): {user_count}")
        print(f"  Employees: {emp_count}")
        print(f"  Managers: {mgr_count}")
        
        # Get sample users
        users = (await session.execute(select(User).limit(3))).scalars().all()
        print(f"\n👥 Sample Users:")
        for u in users:
            print(f"  - {u.email} (role: {u.role})")

asyncio.run(main())
