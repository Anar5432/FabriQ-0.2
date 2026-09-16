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

# Get tables with data
cursor.execute('''
    SELECT t.name
    FROM sys.tables t
    JOIN sys.partitions p ON t.object_id = p.object_id
    WHERE t.is_ms_shipped = 0 AND p.index_id IN (0,1)
    GROUP BY t.name
    HAVING SUM(p.rows) > 0
''')
active_tables = {r.name for r in cursor.fetchall()}

# Now generate DBML only for these active tables
cursor.execute('''
    SELECT t.name as table_name, c.name as column_name, ty.name as data_type, c.is_identity
    FROM sys.tables t
    JOIN sys.columns c ON t.object_id = c.object_id
    JOIN sys.types ty ON c.user_type_id = ty.user_type_id
    WHERE t.is_ms_shipped = 0
    ORDER BY t.name, c.column_id
''')
tables = {}
for row in cursor.fetchall():
    if row.table_name in active_tables:
        if row.table_name not in tables:
            tables[row.table_name] = []
        tables[row.table_name].append({
            'col': row.column_name,
            'type': row.data_type,
            'is_pk': row.is_identity
        })

cursor.execute('''
    SELECT 
        tp.name 'ParentTable',
        cp.name,
        tr.name 'RefTable',
        cr.name
    FROM sys.foreign_keys fk
    INNER JOIN sys.tables tp ON fk.parent_object_id = tp.object_id
    INNER JOIN sys.tables tr ON fk.referenced_object_id = tr.object_id
    INNER JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id = fk.object_id
    INNER JOIN sys.columns cp ON fkc.parent_column_id = cp.column_id AND fkc.parent_object_id = cp.object_id
    INNER JOIN sys.columns cr ON fkc.referenced_column_id = cr.column_id AND fkc.referenced_object_id = cr.object_id
''')
fks = []
for row in cursor.fetchall():
    if row[0] in active_tables and row[2] in active_tables:
        fks.append((row[0], row[1], row[2], row[3]))

out = []
for tname, cols in tables.items():
    out.append(f'Table "{tname}" {{')
    for c in cols:
        pk_str = ' [primary key]' if c['is_pk'] else ''
        col_name = c['col'].replace(' ', '_')
        out.append(f'  "{col_name}" {c["type"]}{pk_str}')
    out.append('}')
    out.append('')
    
for fk in fks:
    out.append(f'Ref: "{fk[0]}"."{fk[1]}" > "{fk[2]}"."{fk[3]}"')

dbml_text = '\n'.join(out)
out_path = 'C:/Users/User/.gemini/antigravity/scratch/backend/BTFERPDB_Active_Schema.dbml'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(dbml_text)
    
print(f"Active tables: {len(active_tables)}")
print("Filtered DBML written to", out_path)
