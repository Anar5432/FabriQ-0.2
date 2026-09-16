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

green_tables = {
    'sm_kontr_sat', 'sm_kontr_sat_el', 'sm_goods', 'sm_process_iz', 
    'sm_process_iz_el', 'sm_sob_trans_el', 'sm_kontr', 'sm_sob_trans',
    'hm_goods', 'hm_kontr'
}

def get_color_info(t):
    if t in green_tables:
        return '#28a745', '🟢 GREEN: Used actively in the dashboard program'
    elif table_rows.get(t, 0) == 0:
        return '#dc3545', '🔴 RED: Old / Not Used (Zero data inside)'
    else:
        return '#007bff', '🔵 BLUE: Actively used by factory, but not in dashboard'

# Find key roots that are important
key_roots = [r for r in roots if r in green_tables or any(c in green_tables for c in children.get(r, []))]
if not key_roots:
    key_roots = roots[:10]

# Add a few more important roots if they are missing
extra = ['sm_good_ist', 'sm_smeta', 'users']
for e in extra:
    if e in roots and e not in key_roots:
        key_roots.append(e)

# Create a folder for these diagrams
out_dir = 'C:/Users/User/.gemini/antigravity/scratch/backend/Database_Diagrams'
os.makedirs(out_dir, exist_ok=True)

# Fetch all columns at once for speed
cursor.execute('''
    SELECT t.name as table_name, c.name as column_name, ty.name as data_type, c.is_identity
    FROM sys.tables t
    JOIN sys.columns c ON t.object_id = c.object_id
    JOIN sys.types ty ON c.user_type_id = ty.user_type_id
    WHERE t.is_ms_shipped = 0
    ORDER BY t.name, c.column_id
''')
all_cols = {}
for row in cursor.fetchall():
    if row.table_name not in all_cols:
        all_cols[row.table_name] = []
    all_cols[row.table_name].append({
        'col': row.column_name,
        'type': row.data_type,
        'is_pk': row.is_identity
    })

# Fetch specific FK column mappings
cursor.execute('''
    SELECT tp.name, cp.name, tr.name, cr.name
    FROM sys.foreign_keys fk
    INNER JOIN sys.tables tp ON fk.parent_object_id = tp.object_id
    INNER JOIN sys.tables tr ON fk.referenced_object_id = tr.object_id
    INNER JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id = fk.object_id
    INNER JOIN sys.columns cp ON fkc.parent_column_id = cp.column_id AND fkc.parent_object_id = cp.object_id
    INNER JOIN sys.columns cr ON fkc.referenced_column_id = cr.column_id AND fkc.referenced_object_id = cr.object_id
''')
all_fk_cols = []
for row in cursor.fetchall():
    all_fk_cols.append((row[0], row[1], row[2], row[3]))

for root in key_roots:
    nodes_to_draw = set()
    edges_to_draw = []
    
    # 3-level extraction
    nodes_to_draw.add(root)
    # L1
    for c1 in children[root]:
        nodes_to_draw.add(c1)
        edges_to_draw.append((root, c1))
        # L2
        for c2 in children[c1]:
            nodes_to_draw.add(c2)
            edges_to_draw.append((c1, c2))

    out = []
    for t in nodes_to_draw:
        color_hex, note = get_color_info(t)
        out.append(f'Table "{t}" [headercolor: {color_hex}] {{')
        if t in all_cols:
            for c in all_cols[t]:
                pk_str = ' [primary key]' if c['is_pk'] else ''
                c_name = c['col'].replace(' ', '_')
                out.append(f'  "{c_name}" {c["type"]}{pk_str}')
        out.append(f"  Note: '{note}'")
        out.append('}')
        out.append('')

    for p, cp, c, cc in all_fk_cols:
        if p in nodes_to_draw and c in nodes_to_draw:
            # Check if this edge was explicitly part of our 3-level tree from this root
            if (p, c) in edges_to_draw:
                out.append(f'Ref: "{p}"."{cp}" > "{c}"."{cc}"')

    # Add a TableGroup to visually bind them
    out.append('')
    out.append(f'TableGroup {root}_Hierarchy {{')
    for n in nodes_to_draw:
        out.append(f'  "{n}"')
    out.append('}')
    
    filename = f"Domain_{root}.dbml"
    with open(os.path.join(out_dir, filename), 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))

print(f"Generated {len(key_roots)} separate diagram files in {out_dir}")
