"""
Seed a small set of demo products across existing categories/subcategories.

This script is idempotent-ish: it checks for existing products with the same
title under the same subcategory before inserting. It assigns sellers in a
round-robin from demo seller accounts (emails starting with 'seller').
"""

from __future__ import annotations

import random
from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.persistance.async_base import AsyncSessionLocal
from backend.persistance.user import User
from backend.persistance.category import Category
from backend.persistance.subcategory import Subcategory
from backend.persistance.product import Product


PRODUCT_TITLES = [
    "Wireless Headphones",
    "Gaming Keyboard",
    "Stainless Steel Water Bottle",
    "Cotton T-Shirt",
    "LED Desk Lamp",
    "Bluetooth Speaker",
    "Yoga Mat",
    "Ceramic Coffee Mug",
    "Portable Charger",
    "Running Shoes",
]


from sqlalchemy.ext.asyncio import AsyncSession

async def pick_sellers(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).where(User.email.like("seller%")))
    sellers = result.scalars().all()
    if not sellers:
        result = await session.execute(select(User))
        sellers = result.scalars().all()
    return list(sellers)


async def existing_titles_in_sub(session: AsyncSession, subcat_id: int) -> set[str]:
    result = await session.execute(
        select(Product.title).where(Product.subcategory_id == subcat_id)
    )
    rows = result.all()
    return {t for (t,) in rows}


async def seed_products_for_subcategory(session: AsyncSession, sub: Subcategory, sellers: list[User], max_per_sub: int = 5) -> int:
    if not sellers:
        return 0
    existing = await existing_titles_in_sub(session, sub.subcategory_id)
    count = 0
    titles = PRODUCT_TITLES[:]
    random.shuffle(titles)
    for i in range(min(max_per_sub, len(titles))):
        title = titles[i]
        if title in existing:
            continue
        seller = sellers[count % len(sellers)]
        price_cents = random.randint(999, 9999)
        price = Decimal(price_cents) / Decimal(100)
        p = Product(
            seller_id=seller.user_id,
            category_id=sub.category_id,
            subcategory_id=sub.subcategory_id,
            title=title,
            description=f"Demo {title} in {sub.name}",
            price=price,
            currency="USD",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(p)
        try:
            await session.flush()
            count += 1
        except IntegrityError:
            await session.rollback()
            continue
    return count


import asyncio
async def main() -> None:
    total = 0
    async with AsyncSessionLocal() as session:
        sellers = await pick_sellers(session)
        result = await session.execute(select(Subcategory).order_by(Subcategory.subcategory_id))
        subcats = result.scalars().all()
        for sub in subcats:
            total += await seed_products_for_subcategory(session, sub, sellers, max_per_sub=3)
        await session.commit()
    print(f"Seeded demo products: {total}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
