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
fks_raw = set()
for r in cursor.fetchall():
    fks_raw.add((r.Parent, r.Child))

all_tables = set(table_rows.keys())
children = {t: set() for t in all_tables}
parents = {t: set() for t in all_tables}

for p, c in fks_raw:
    if p in all_tables and c in all_tables:
        children[p].add(c)
        parents[c].add(p)

roots = [t for t in all_tables if len(parents[t]) == 0 and len(children[t]) > 0]

# Dashboard Tables (Green)
green_tables = {
    'sm_kontr_sat', 'sm_kontr_sat_el', 'sm_goods', 'sm_process_iz', 
    'sm_process_iz_el', 'sm_sob_trans_el', 'sm_kontr', 'sm_sob_trans',
    'hm_goods', 'hm_kontr'
}

def get_color(t):
    if t in green_tables:
        return '#28a745' # Green
    elif table_rows.get(t, 0) == 0:
        return '#dc3545' # Red
    else:
        return '#007bff' # Blue

# Find key roots up to 3 levels
key_roots = [r for r in roots if r in green_tables or any(c in green_tables for c in children[r])]
if not key_roots:
    key_roots = roots[:10]

nodes_to_draw = set()
edges_to_draw = []

for r in key_roots:
    nodes_to_draw.add(r)
    # Level 1
    for c1 in children[r]:
        nodes_to_draw.add(c1)
        edges_to_draw.append((r, c1))
        # Level 2
        for c2 in children[c1]:
            nodes_to_draw.add(c2)
            edges_to_draw.append((c1, c2))

# Fetch columns only for nodes_to_draw to make valid DBML
cols_by_table = {t: [] for t in nodes_to_draw}
cursor.execute('''
    SELECT t.name as table_name, c.name as column_name, ty.name as data_type, c.is_identity
    FROM sys.tables t
    JOIN sys.columns c ON t.object_id = c.object_id
    JOIN sys.types ty ON c.user_type_id = ty.user_type_id
    WHERE t.is_ms_shipped = 0
    ORDER BY t.name, c.column_id
''')
for row in cursor.fetchall():
    if row.table_name in nodes_to_draw:
        cols_by_table[row.table_name].append({
            'col': row.column_name,
            'type': row.data_type,
            'is_pk': row.is_identity
        })

out = []
for t in nodes_to_draw:
    color = get_color(t)
    out.append(f'Table "{t}" [headercolor: {color}] {{')
    for c in cols_by_table[t]:
        pk_str = ' [primary key]' if c['is_pk'] else ''
        c_name = c['col'].replace(' ', '_')
        out.append(f'  "{c_name}" {c["type"]}{pk_str}')
    out.append('}')
    out.append('')

# Only output edges that exist between our selected nodes
for p, c in edges_to_draw:
    # We need to find the actual columns for the foreign key to make dbdiagram happy, 
    # but a simple hack for dbdiagram is to just link any column. Let's find the real columns.
    pass

cursor.execute('''
    SELECT tp.name, cp.name, tr.name, cr.name
    FROM sys.foreign_keys fk
    INNER JOIN sys.tables tp ON fk.parent_object_id = tp.object_id
    INNER JOIN sys.tables tr ON fk.referenced_object_id = tr.object_id
    INNER JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id = fk.object_id
    INNER JOIN sys.columns cp ON fkc.parent_column_id = cp.column_id AND fkc.parent_object_id = cp.object_id
    INNER JOIN sys.columns cr ON fkc.referenced_column_id = cr.column_id AND fkc.referenced_object_id = cr.object_id
''')
for row in cursor.fetchall():
    if row[0] in nodes_to_draw and row[2] in nodes_to_draw:
        # DBML syntax: Ref: "child"."child_col" > "parent"."parent_col"
        out.append(f'Ref: "{row[0]}"."{row[1]}" > "{row[2]}"."{row[3]}"')

out_path = 'C:/Users/User/.gemini/antigravity/scratch/backend/Colored_Hierarchy_Schema.dbml'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print("Colored DBML generated!")
