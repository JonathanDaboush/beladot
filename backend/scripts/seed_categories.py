from typing import Dict, List
from sqlalchemy import select, func

from backend.db.init_schema import ensure_sqlite_schema
from backend.persistance.base import get_sessionmaker
from backend.persistance.category import Category
from backend.persistance.subcategory import Subcategory


CATEGORY_TREE: Dict[str, List[str]] = {
    "Electronics": [
        "Mobile Phones",
        "Laptops",
        "Consoles",
        "Cameras",
        "Headphones",
        "Smart Home",
    ],
    "Computers": [
        "Desktops",
        "Monitors",
        "Keyboards",
        "Mice",
        "Components",
    ],
    "Home & Kitchen": [
        "Appliances",
        "Cookware",
        "Furniture",
        "Home Decor",
        "Storage & Organization",
    ],
    "Fashion": [
        "Men",
        "Women",
        "Kids",
        "Shoes",
        "Accessories",
    ],
    "Beauty": [
        "Makeup",
        "Skincare",
        "Hair Care",
        "Fragrance",
    ],
    "Sports": [
        "Fitness",
        "Outdoor",
        "Team Sports",
        "Cycling",
    ],
    "Toys & Games": [
        "Board Games",
        "Action Figures",
        "Puzzles",
        "STEM Toys",
    ],
    "Books": [
        "Fiction",
        "Non-Fiction",
        "Comics & Manga",
        "Children's Books",
    ],
}


def _next_id(session, model, pk_attr):
    current_max = session.execute(select(func.max(pk_attr))).scalar()
    return (current_max or 0) + 1


def main():
    ensure_sqlite_schema()
    Session = get_sessionmaker()
    created_summary = []
    with Session() as session:
        # Load existing categories by name
        existing_cats = {
            c.name: c for c in session.execute(select(Category)).scalars().all()
        }

        for cat_name, subs in CATEGORY_TREE.items():
            cat = existing_cats.get(cat_name)
            if not cat:
                cat_id = _next_id(session, Category, Category.category_id)
                cat = Category(category_id=cat_id, name=cat_name, image_url=None)
                session.add(cat)
                session.flush()
                existing_cats[cat_name] = cat

            # Ensure subcategories
            existing_subs = {
                s.name: s
                for s in session.execute(
                    select(Subcategory).where(Subcategory.category_id == cat.category_id)
                ).scalars().all()
            }
            created_subs = []
            for sub_name in subs:
                if sub_name not in existing_subs:
                    sub_id = _next_id(session, Subcategory, Subcategory.subcategory_id)
                    s = Subcategory(
                        subcategory_id=sub_id,
                        category_id=cat.category_id,
                        name=sub_name,
                        image_url=None,
                    )
                    session.add(s)
                    session.flush()
                    existing_subs[sub_name] = s
                    created_subs.append(sub_name)
            if created_subs:
                created_summary.append((cat.name, created_subs))

        session.commit()

    print("\n=== Seeded Categories & Subcategories ===")
    if not created_summary:
        print("No new categories/subcategories were created (already present).")
    else:
        for cat_name, subs in created_summary:
            print(f"{cat_name}:")
            for s in subs:
                print(f"  - {s}")


if __name__ == "__main__":
    main()
