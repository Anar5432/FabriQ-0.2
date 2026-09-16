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

cursor.execute('''
    SELECT t.name, SUM(p.rows) as rcount
    FROM sys.tables t
    JOIN sys.partitions p ON t.object_id = p.object_id
    WHERE t.is_ms_shipped = 0 AND p.index_id IN (0,1)
    GROUP BY t.name
''')
table_rows = {r.name: r.rcount for r in cursor.fetchall()}

cursor.execute('''
    SELECT tp.name 'Parent', tr.name 'Child'
    FROM sys.foreign_keys fk
    INNER JOIN sys.tables tp ON fk.referenced_object_id = tp.object_id
    INNER JOIN sys.tables tr ON fk.parent_object_id = tr.object_id
''')
fks = set()
for r in cursor.fetchall():
    fks.add((r.Parent, r.Child))

all_tables = set(table_rows.keys())
children = {t: set() for t in all_tables}
parents = {t: set() for t in all_tables}

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

def get_color(t):
    if t in green_tables:
        return 'green'
    elif table_rows.get(t, 0) == 0:
        return 'red'
    else:
        return 'blue'

# We'll create multiple subgraphs to prevent one giant unreadable mermaid blob.
# Group roots by domain or just output the biggest ones.
md = ["# Database Architecture (3-Level Hierarchy)"]
md.append("> [!TIP]")
md.append("> **Color Legend:**")
md.append("> 🟢 **Green**: Actively used by our Dashboard program right now.")
md.append("> 🔵 **Blue**: Actively used by the factory (has data), but not shown on Dashboard.")
md.append("> 🔴 **Red**: Old/Unused (Zero data inside).")

# Select the top 10 most heavily connected roots + any green roots to avoid rendering crashes
selected_roots = roots[:15]
for g in green_tables:
    if g in roots and g not in selected_roots:
        selected_roots.append(g)

for root in selected_roots:
    md.append(f"## Domain: {root}")
    md.append("```mermaid")
    md.append("graph TD")
    
    # define classes
    md.append("classDef green fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724;")
    md.append("classDef blue fill:#cce5ff,stroke:#007bff,stroke-width:2px,color:#004085;")
    md.append("classDef red fill:#f8d7da,stroke:#dc3545,stroke-width:2px,color:#721c24;")
    
    nodes = set()
    edges = []
    
    # Level 0
    nodes.add(root)
    # Level 1
    for c1 in children[root]:
        nodes.add(c1)
        edges.append((root, c1))
        # Level 2
        for c2 in children[c1]:
            nodes.add(c2)
            edges.append((c1, c2))
            
    for n in nodes:
        c_name = get_color(n)
        md.append(f"{n}:::{c_name}")
        
    for p, c in edges:
        md.append(f"{p} --> {c}")
        
    md.append("```\n")

out_path = 'C:/Users/User/.gemini/antigravity/brain/ec3ddb91-de40-4446-bb2f-79bdd5cae722/database_graphic.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\\n'.join(md))
print("Graphic created!")
