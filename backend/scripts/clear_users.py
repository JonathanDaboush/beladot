
import asyncio
from sqlalchemy import delete
from backend.persistance.async_base import AsyncSessionLocal
from backend.persistance.user import User

async def main() -> None:
    async with AsyncSessionLocal() as session:
        await session.execute(delete(User))
        await session.commit()
    print("Cleared all users from users table.")

if __name__ == "__main__":
    asyncio.run(main())
