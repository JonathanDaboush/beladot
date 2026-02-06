import os
import re
import shutil
from typing import Dict, List, Tuple
from difflib import SequenceMatcher


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.persistance.async_base import AsyncSessionLocal
from backend.db.init_schema import ensure_sqlite_schema
from backend.persistance.user import User
from backend.persistance.category import Category
from backend.persistance.subcategory import Subcategory


IMAGES_ROOT = os.path.join("backend", "images")
USER_IMAGES_DIR = os.path.join(IMAGES_ROOT, "user_images")
# Support multiple possible folders for category/subcategory images
CATS_DIR_CANDIDATES = [
    os.path.join(IMAGES_ROOT, "categories and subcategories"),
    os.path.join(IMAGES_ROOT, "subcategories"),
    os.path.join(IMAGES_ROOT, "categories"),
]


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

def tokenize(s: str) -> List[str]:
    s = s.lower()
    s = s.replace("&", "and")
    s = s.replace("'", "")
    s = s.replace("-", " ")
    s = s.replace("_", " ")
    s = re.sub(r"\s+", " ", s).strip()
    # Basic tokenization by spaces
    return [t for t in s.split(" ") if t]


def similar(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def build_file_entries(folders) -> List[Tuple[str, str, List[str], str]]:
    """Return list of (display_base, rel_path, tokens, compact) from folders."""
    if isinstance(folders, str):
        folders = [folders]
    out: List[Tuple[str, str, List[str], str]] = []
    for folder in folders:
        if not os.path.isdir(folder):
            continue
        for name in os.listdir(folder):
            path = os.path.join(folder, name)
            if not os.path.isfile(path):
                continue
            base, _ext = os.path.splitext(name)
            rel = os.path.join(os.path.relpath(folder, IMAGES_ROOT), name).replace("\\", "/")
            out.append((base, rel, tokenize(base), normalize(base)))
    return out

def jaccard(a: List[str], b: List[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    inter = len(sa & sb)
    union = len(sa | sb)
    return inter / union if union else 0.0

def find_best_entry(name: str, entries: List[Tuple[str, str, List[str], str]]):
    """Return rel_path from entries best matching name, or None."""
    name_compact = normalize(name)
    name_tokens = tokenize(name)
    # 1) Exact compact match
    for _base, rel, _tok, compact in entries:
        if compact == name_compact:
            return rel
    # 2) Exact token-set match
    name_set = set(name_tokens)
    for _base, rel, tok, _compact in entries:
        if set(tok) == name_set:
            return rel
    # 3) Best combined score: favor token overlap strongly
    best_rel = None
    best_score = 0.0
    for _base, rel, tok, compact in entries:
        jac = jaccard(name_tokens, tok)
        if jac == 0:
            continue  # avoid unrelated partials like keyboards vs board games
        seq = similar(name_compact, compact)
        score = 0.7 * jac + 0.3 * seq
        if score > best_score:
            best_score = score
            best_rel = rel
    # Require reasonably high confidence to avoid wrong mappings
    if best_rel and best_score >= 0.75:
        return best_rel
    return None


def build_file_index(folders) -> Dict[str, str]:
    # Kept for compatibility if used elsewhere
    entries = build_file_entries(folders)
    idx: Dict[str, str] = {}
    for _base, rel, _tok, compact in entries:
        idx.setdefault(compact, rel)
    return idx


def safe_email_filename(email: str) -> str:
    base = re.sub(r"[^a-zA-Z0-9]+", "_", email)
    return base + ".jpg"


async def assign_user_images(session: AsyncSession):
    files = [f for f in os.listdir(USER_IMAGES_DIR) if os.path.isfile(os.path.join(USER_IMAGES_DIR, f))]
    files.sort()
    if not files:
        return []
    users = [u async for u in (await session.stream_scalars(select(User).order_by(User.email)))]
    assigned = []
    for i, u in enumerate(users):
        src_name = files[i % len(files)]
        dst_name = safe_email_filename(u.email)
        src_path = os.path.join(USER_IMAGES_DIR, src_name)
        dst_path = os.path.join(USER_IMAGES_DIR, dst_name)
        if os.path.abspath(src_path) != os.path.abspath(dst_path):
            shutil.copyfile(src_path, dst_path)
        u.img_location = os.path.join("images", "user_images", dst_name)
        assigned.append((u.email, u.img_location))
    await session.flush()
    return assigned


async def assign_category_images(session: AsyncSession):
    entries = build_file_entries(CATS_DIR_CANDIDATES)
    updated = []
    cats = [c async for c in (await session.stream_scalars(select(Category)))]
    for c in cats:
        rel_path = find_best_entry(c.name or "", entries)
        if rel_path:
            c.image_url = rel_path.replace("\\", "/")
            updated.append((c.name, c.image_url))
    await session.flush()
    return updated


async def assign_subcategory_images(session: AsyncSession):
    entries = build_file_entries(CATS_DIR_CANDIDATES)
    updated = []
    subs = [s async for s in (await session.stream_scalars(select(Subcategory)))]
    for s in subs:
        rel_path = find_best_entry(s.name or "", entries)
        if rel_path:
            s.image_url = rel_path.replace("\\", "/")
            updated.append((s.name, s.image_url))
    await session.flush()
    return updated


async def _get_used_paths(session: AsyncSession) -> set[str]:
    used = set()
    for p in [v async for v in (await session.stream_scalars(select(Category.image_url)))]:
        if p:
            used.add(p)
    for p in [v async for v in (await session.stream_scalars(select(Subcategory.image_url)))]:
        if p:
            used.add(p)
    return used


async def assign_prefer_unused_for_targets(session: AsyncSession, target_category_names: list[str]):
    """
    For specified categories (by name) and their subcategories, fill only MISSING images
    by preferring entries whose images are currently unused anywhere.
    """
    entries = build_file_entries(CATS_DIR_CANDIDATES)
    used = await _get_used_paths(session)
    # Build a list of candidate entries that are not used
    unused_entries = [e for e in entries if e[1] not in used]

    # Helper to pick from unused first; fallback to full entries if needed
    def pick(name: str) -> str | None:
        rel = find_best_entry(name, unused_entries)
        if rel:
            return rel
        return find_best_entry(name, entries)

    # Categories first
    cats = [c async for c in (await session.stream_scalars(select(Category).where(Category.name.in_(target_category_names))))]
    for c in cats:
        if not c.image_url:
            rel = pick(c.name or "")
            if rel:
                c.image_url = rel.replace("\\", "/")
                img_url = c.image_url
                if img_url:  # Type narrowing
                    used.add(img_url)
    await session.flush()

    # Subcategories under those categories (Electronics, Computers, etc.)
    if cats:
        cat_ids = [c.category_id for c in cats]
        subs = [s async for s in (await session.stream_scalars(select(Subcategory).where(Subcategory.category_id.in_(cat_ids))))]
        for s in subs:
            if not s.image_url:
                rel = pick(s.name or "")
                if rel:
                    s.image_url = rel.replace("\\", "/")
                    img_url = s.image_url
                    if img_url:  # Type narrowing
                        used.add(img_url)
        await session.flush()


import asyncio

async def main() -> None:
    ensure_sqlite_schema()
    async with AsyncSessionLocal() as session:
        user_assign = await assign_user_images(session)
        cat_assign = await assign_category_images(session)
        sub_assign = await assign_subcategory_images(session)
        await session.commit()

    print("\n=== Image Assignment Summary ===")
    print(f"Users updated: {len(user_assign)}")
    print(f"Categories updated: {len(cat_assign)}")
    print(f"Subcategories updated: {len(sub_assign)}")

if __name__ == "__main__":
    asyncio.run(main())
