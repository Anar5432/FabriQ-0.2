import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
import pyodbc
from django.conf import settings
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
django.setup()

conn_str = f"DRIVER={{{settings.MSSQL_CONFIG['DRIVER']}}};SERVER={settings.MSSQL_CONFIG['SERVER']};DATABASE=BTFERPDB;UID={settings.MSSQL_CONFIG['USERNAME']};PWD={settings.MSSQL_CONFIG['PASSWORD']};TrustServerCertificate=yes;Encrypt=no;"
conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()

# Get row counts
cursor.execute('''
    SELECT t.name, SUM(p.rows) as rcount
    FROM sys.tables t
    JOIN sys.partitions p ON t.object_id = p.object_id
    WHERE t.is_ms_shipped = 0 AND p.index_id IN (0,1)
    GROUP BY t.name
''')
table_rows = {r.name: r.rcount for r in cursor.fetchall()}

# Get foreign keys
cursor.execute('''
    SELECT tp.name 'Parent', tr.name 'Child'
    FROM sys.foreign_keys fk
    INNER JOIN sys.tables tp ON fk.referenced_object_id = tp.object_id
    INNER JOIN sys.tables tr ON fk.parent_object_id = tr.object_id
''')
# Note: tp is the referenced object (Parent), tr is the referencing object (Child).
fks = set()
for r in cursor.fetchall():
    fks.add((r.Parent, r.Child))

children = {}
parents = {}
all_tables = set(table_rows.keys())
for t in all_tables:
    children[t] = set()
    parents[t] = set()

for p, c in fks:
    if p in all_tables and c in all_tables:
        children[p].add(c)
        parents[c].add(p)

roots = [t for t in all_tables if len(parents[t]) == 0 and len(children[t]) > 0]
roots.sort(key=lambda t: len(children[t]), reverse=True)

# Dashboard Tables (Green)
green_tables = {
    'sm_kontr_sat', 'sm_kontr_sat_el', 'sm_goods', 'sm_process_iz', 
    'sm_process_iz_el', 'sm_sob_trans_el', 'sm_kontr', 'sm_sob_trans',
    'hm_goods', 'hm_kontr'
}

print(f"Total tables: {len(all_tables)}")
print(f"Total roots: {len(roots)}")

# Explore 3 levels starting from key roots that connect to our green tables
# Let's find roots that are ancestors of green tables.
ancestor_of_green = set()
def find_green(t, depth=0):
    if depth > 5: return False
    if t in green_tables: return True
    for c in children[t]:
        if find_green(c, depth+1):
            return True
    return False

key_roots = [r for r in roots if find_green(r)]
print(f"Key roots that lead to green tables: {len(key_roots)}")

# Collect up to 3 levels from these key roots
collected = set()
edges = []
for r in key_roots:
    collected.add(r)
    # L1
    for c1 in children[r]:
        collected.add(c1)
        edges.append((r, c1))
        # L2
        for c2 in children[c1]:
            collected.add(c2)
            edges.append((c1, c2))
            
print(f"Total nodes in top 3 levels of key domains: {len(collected)}")
print(f"Total edges: {len(edges)}")
