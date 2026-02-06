import re
from pathlib import Path

p = Path('backend/persistance')
py_files = list(p.glob('*.py'))
fk_re = re.compile(r"ForeignKey\('\s*([a-zA-Z0-9_]+)\.")
table_re = re.compile(r"__tablename__\s*=\s*['\"]([a-zA-Z0-9_]+)['\"]")

fk_tables = set()
tables = set()

for f in py_files:
    txt = f.read_text(encoding='utf-8')
    for m in fk_re.finditer(txt):
        fk_tables.add(m.group(1))
    for m in table_re.finditer(txt):
        tables.add(m.group(1))

print('Found __tablename__ values:')
for t in sorted(tables):
    print('  ', t)

print('\nFound ForeignKey target tables:')
for t in sorted(fk_tables):
    print('  ', t)

missing = sorted([t for t in fk_tables if t not in tables])
print('\nForeignKey targets missing matching __tablename__:')
for t in missing:
    print('  ', t)

if not missing:
    print('\nNo mismatches detected.')
