import os
import re
import shutil
from typing import Dict

from sqlalchemy import select

from backend.persistance.base import get_sessionmaker
from backend.db.init_schema import ensure_sqlite_schema
from backend.persistance.user import User
from backend.persistance.category import Category
from backend.persistance.subcategory import Subcategory


IMAGES_ROOT = os.path.join("backend", "images")
USER_IMAGES_DIR = os.path.join(IMAGES_ROOT, "user_images")
CATS_DIR = os.path.join(IMAGES_ROOT, "categories and subcategories")


def normalize(s: str) -> str:
    s = s.lower()
    s = s.replace("&", "and")
    s = s.replace("'", "")
    s = s.replace("-", " ")
    s = s.replace("_", " ")
    s = re.sub(r"\s+", " ", s).strip()
    # Common corrections
    corrections = {
        "wemon": "women",
        "fragrence": "fragrance",
        "skin care": "skincare",
        "non fiction": "nonfiction",
        "comics and manga": "comics and manga",  # stays; matched against name similarly
        "home and kitchen": "home and kitchen",
        "storage and organization": "storage and organization",
        "toys and games": "toys and games",
    }
    s = corrections.get(s, s)
    # Remove spaces for final key to be robust
    s = s.replace(" ", "")
    return s


def build_file_index(folder: str) -> Dict[str, str]:
    idx: Dict[str, str] = {}
    if not os.path.isdir(folder):
        return idx
    for name in os.listdir(folder):
        path = os.path.join(folder, name)
        if not os.path.isfile(path):
            continue
        base, ext = os.path.splitext(name)
        key = normalize(base)
        idx[key] = name  # store original filename
    return idx


def safe_email_filename(email: str) -> str:
    base = re.sub(r"[^a-zA-Z0-9]+", "_", email)
    return base + ".jpg"


def assign_user_images(session):
    files = [f for f in os.listdir(USER_IMAGES_DIR) if os.path.isfile(os.path.join(USER_IMAGES_DIR, f))]
    files.sort()
    if not files:
        return []
    users = session.execute(select(User).order_by(User.email)).scalars().all()
    assigned = []
    for i, u in enumerate(users):
        src_name = files[i % len(files)]
        dst_name = safe_email_filename(u.email)
        src_path = os.path.join(USER_IMAGES_DIR, src_name)
        dst_path = os.path.join(USER_IMAGES_DIR, dst_name)
        # Copy or overwrite to ensure filename reflects the email
        shutil.copyfile(src_path, dst_path)
        u.img_location = os.path.join("images", "user_images", dst_name)
        assigned.append((u.email, u.img_location))
    session.flush()
    return assigned


def assign_category_images(session):
    file_index = build_file_index(CATS_DIR)
    updated = []
    cats = session.execute(select(Category)).scalars().all()
    for c in cats:
        key = normalize(c.name)
        fname = file_index.get(key)
        if fname:
            c.image_url = os.path.join("images", "categories and subcategories", fname)
            updated.append((c.name, c.image_url))
    session.flush()
    return updated


def assign_subcategory_images(session):
    file_index = build_file_index(CATS_DIR)
    updated = []
    subs = session.execute(select(Subcategory)).scalars().all()
    for s in subs:
        key = normalize(s.name)
        fname = file_index.get(key)
        if fname:
            s.image_url = os.path.join("images", "categories and subcategories", fname)
            updated.append((s.name, s.image_url))
    session.flush()
    return updated


def main():
    ensure_sqlite_schema()
    Session = get_sessionmaker()
    with Session() as session:
        user_assign = assign_user_images(session)
        cat_assign = assign_category_images(session)
        sub_assign = assign_subcategory_images(session)
        session.commit()

    print("\n=== Image Assignment Summary ===")
    print(f"Users updated: {len(user_assign)}")
    print(f"Categories updated: {len(cat_assign)}")
    print(f"Subcategories updated: {len(sub_assign)}")

    # Show a few examples
    for role, (name, path_list) in {
        "Category": (cat_assign[:5], ""),
        "Subcategory": (sub_assign[:5], ""),
    }.items():
        pass


if __name__ == "__main__":
    main()
