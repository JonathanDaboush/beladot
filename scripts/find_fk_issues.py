import re
import glob
import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'backend' / 'persistance'
py_files = sorted(glob.glob(str(p / '*.py')))

tablenames = {}
fk_refs = []

re_tab = re.compile(r"__tablename__\s*=\s*['\"]([a-zA-Z0-9_]+)['\"]")
re_fk = re.compile(r"ForeignKey\(([^)]+)\)")
re_str = re.compile(r"['\"]([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)['\"]")

for f in py_files:
    text = Path(f).read_text(encoding='utf-8')
    m = re_tab.search(text)
    if m:
        tablenames[m.group(1)] = f
    for i, line in enumerate(text.splitlines(), start=1):
        if 'ForeignKey' in line:
            m = re_fk.search(line)
            if m:
                arg = m.group(1)
                ms = re_str.search(arg)
                if ms:
                    table = ms.group(1)
                    col = ms.group(2)
                else:
                    table = arg.strip().strip("'\"")
                    col = None
                fk_refs.append({'file': f, 'line': i, 'table': table, 'col': col, 'code': line.strip()})

output = {'tablenames': tablenames, 'fk_refs': fk_refs}
print(json.dumps(output, indent=2))
