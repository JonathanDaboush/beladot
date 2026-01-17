import os
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "frontend" / "src"
EXTS = [".js", ".jsx", ".ts", ".tsx", ".json"]

IMPORT_RE = re.compile(r"^\s*import\s+(?:[^'\"]+\s+from\s+)?['\"](\.[^'\"]+)['\"]", re.MULTILINE)
REQ_RE = re.compile(r"require\(\s*['\"](\.[^'\"]+)['\"]\s*\)")

missing = []

for path in SRC.rglob("*.js"):
    text = path.read_text(encoding="utf-8", errors="ignore")
    rels = IMPORT_RE.findall(text) + REQ_RE.findall(text)
    for rel in rels:
        # skip CSS/images
        if any(rel.endswith(ext) for ext in [".css", ".png", ".jpg", ".jpeg", ".svg", ".gif"]):
            continue
        target = (path.parent / rel).resolve()
        if target.is_file():
            continue
        # try index resolution and extensions
        found = False
        for ext in EXTS:
            if target.with_suffix(ext).is_file():
                found = True
                break
            index_path = target / ("index" + ext)
            if index_path.is_file():
                found = True
                break
        if not found:
            missing.append((str(path.relative_to(SRC)), rel))

print("Missing frontend imports:")
for f, rel in missing:
    print(f"- {f} -> {rel}")
print(f"Total: {len(missing)} missing")
