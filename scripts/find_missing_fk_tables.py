import json,sys
from pathlib import Path
j = json.loads(Path('scripts/find_fk_issues.py').read_text()) if False else None
# reuse previous script output by running it
import subprocess, json
proc = subprocess.run(['python','scripts/find_fk_issues.py'], capture_output=True, text=True)
if proc.returncode != 0:
    print(proc.stderr)
    sys.exit(1)
data = json.loads(proc.stdout)
tablenames = set(data['tablenames'].keys())
missing = [fk for fk in data['fk_refs'] if fk['table'] not in tablenames]
print(json.dumps({'missing': missing, 'count': len(missing)}, indent=2))
