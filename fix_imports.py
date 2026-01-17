import os
import re
from pathlib import Path

ROOT = Path(__file__).parent
TARGET_DIRS = [ROOT / "backend"]

PATTERNS = [
    (re.compile(r"\bfrom\s+backend\.model\."), "from backend.models.model."),
    (re.compile(r"\bimport\s+backend\.model\."), "import backend.models.model."),
    (re.compile(r"\bfrom\s+backend\.repository\."), "from backend.repositories.repository."),
    (re.compile(r"\bimport\s+backend\.repository\."), "import backend.repositories.repository."),
]

changed_files = []

for base in TARGET_DIRS:
    for path in base.rglob("*.py"):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        orig = text
        for pat, repl in PATTERNS:
            text = pat.sub(repl, text)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            changed_files.append(str(path.relative_to(ROOT)))

print("Updated imports in", len(changed_files), "files")
for f in changed_files:
    print(f)
