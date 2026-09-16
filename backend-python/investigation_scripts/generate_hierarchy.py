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
            left = parts[0].split('"')
            child = left[1]
            right = parts[1].split('"')
            parent = right[1]
            fks.append((child, parent))
        except:
            pass

children = {t: set() for t in tables}
parents = {t: set() for t in tables}
for c, p in fks:
    if c in tables and p in tables:
        children[p].add(c)
        parents[c].add(p)

roots = [t for t in tables if len(parents[t]) == 0 and len(children[t]) > 0]
roots.sort(key=lambda t: len(children[t]), reverse=True)

# Generate a hierarchical markdown artifact
md = ["# Database Hierarchical Map\\n"]
md.append("Because this database has almost 400 tables, a traditional diagram will look like a messy spiderweb. Below is a structured, hierarchical view starting from the absolute **Root Parent** tables (the core databases that everything else links to).\\n")

def get_tree(table, depth=0, max_depth=2):
    if depth > max_depth:
        return ""
    
    indent = "    " * depth
    out = ""
    chs = sorted(list(children[table]))
    for c in chs:
        out += f"{indent}- **{c}**\\n"
        out += get_tree(c, depth+1, max_depth)
    return out

for r in roots[:15]:
    md.append(f"### 📦 ROOT: {r} *(Has {len(children[r])} direct child tables)*")
    md.append(get_tree(r, 0, 1)) # Show up to 2 levels deep
    md.append("\\n---\\n")

with open('C:/Users/User/.gemini/antigravity/brain/ec3ddb91-de40-4446-bb2f-79bdd5cae722/hierarchy_map.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md))
print("Hierarchy map created!")
