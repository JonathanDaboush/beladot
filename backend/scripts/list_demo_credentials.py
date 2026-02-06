from sqlalchemy import select
from backend.persistance.async_base import AsyncSessionLocal
from backend.persistance.user import User


def infer_role(email: str) -> str:
    if email.startswith('seller'):
        return 'seller'
    if email.startswith('user'):
        return 'user'
    if email.startswith('customer_service'):
        return 'customer_service'
    if email.startswith('shipping'):
        return 'shipping'
    if email.startswith('finance'):
        return 'finance'
    if email.startswith('mgr_'):
        return 'manager'
    return 'user'


import asyncio
async def main() -> None:
    async with AsyncSessionLocal() as s:
        result = await s.execute(select(User.full_name, User.email, User.password).order_by(User.email))
        rows = result.all()
    for name, email, pwd in rows:
        role = infer_role(email)
        print(f"{role}\t{name}\t{email}\t{pwd}")


if __name__ == "__main__":
    asyncio.run(main())
