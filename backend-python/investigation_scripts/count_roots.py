import sys

dbml_path = 'C:/Users/User/.gemini/antigravity/scratch/backend/BTFERPDB_schema.dbml'
with open(dbml_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

tables = set()
fks = []
for line in lines:
    line = line.strip()
    if line.startswith('Table '):
        tname = line.split('"')[1]
        tables.add(tname)
    elif line.startswith('Ref:'):
        try:
            parts = line.split('>')
            child = parts[0].split('"')[1]
            parent = parts[1].split('"')[1]
            fks.append((child, parent))
        except: pass

children = {t: set() for t in tables}
parents = {t: set() for t in tables}
for c, p in fks:
    if c in tables and p in tables:
        children[p].add(c)
        parents[c].add(p)

roots = [t for t in tables if len(parents[t]) == 0 and len(children[t]) > 0]
print(f'Total Root Tables (Heads): {len(roots)}')
