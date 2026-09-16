import os
import sys
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()

from dashboard.erp_connector import get_connection

# Look for table schema modifications in the last 90 days
query = """
SELECT 
    t.name AS TableName, 
    c.name AS ColumnName,
    t.create_date AS CreateDate,
    t.modify_date AS ModifyDate
FROM sys.tables t
LEFT JOIN sys.columns c ON t.object_id = c.object_id
WHERE t.modify_date > DATEADD(day, -90, GETDATE())
ORDER BY t.modify_date DESC, t.name, c.column_id
"""

conn = get_connection()
cursor = conn.cursor(as_dict=True)
cursor.execute(query)
results = cursor.fetchall()

if not results:
    print("No tables modified in the last 90 days.")
else:
    tables = {}
    for r in results:
        tname = r['TableName']
        cname = r['ColumnName']
        if tname not in tables:
            tables[tname] = {'create': r['CreateDate'], 'modify': r['ModifyDate'], 'cols': []}
        if cname:
            tables[tname]['cols'].append(cname)
            
    print("--- RECENT SCHEMA CHANGES (LAST 90 DAYS) ---")
    for tname, tdata in tables.items():
        print(f"\nTable: {tname}")
        print(f"  Created : {tdata['create']}")
        print(f"  Modified: {tdata['modify']}")
        print(f"  Columns : {len(tdata['cols'])}")
