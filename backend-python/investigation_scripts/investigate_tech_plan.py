import os
import sys
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()

from dashboard.erp_connector import get_connection

conn = get_connection()
cursor = conn.cursor(as_dict=True)

print("--- 1. Checking Stored Procedures for sm_tech_plan ---")
query_sp = """
SELECT o.name, o.type_desc 
FROM sys.sql_modules m 
INNER JOIN sys.objects o ON m.object_id = o.object_id 
WHERE m.definition LIKE '%sm_tech_plan%'
"""
cursor.execute(query_sp)
sps = cursor.fetchall()
if not sps:
    print("No stored procedures or views found mentioning 'sm_tech_plan'.")
else:
    for sp in sps:
        print(f"Found {sp['type_desc']}: {sp['name']}")

print("\n--- 2. Checking Columns in sm_mal_say for Reservation Logic ---")
query_cols = """
SELECT c.name, ty.name AS type 
FROM sys.columns c 
JOIN sys.types ty ON c.user_type_id = ty.user_type_id 
WHERE c.object_id = OBJECT_ID('sm_mal_say')
"""
cursor.execute(query_cols)
cols = cursor.fetchall()
for c in cols:
    if any(keyword in c['name'].lower() for keyword in ['rezerv', 'reserve', 'book', 'blok', 'qaliq', 'ehtiyyac', 'plan', 'miqdar', 'sif']):
        print(f"Potential Reservation Column: {c['name']} ({c['type']})")
        
print("\n--- 3. Checking sm_tech_plan table for triggers ---")
query_trig = """
SELECT t.name 
FROM sys.triggers t
WHERE t.parent_id = OBJECT_ID('sm_tech_plan') OR t.parent_id = OBJECT_ID('sm_tech_plan_xammal')
"""
cursor.execute(query_trig)
trigs = cursor.fetchall()
for t in trigs:
    print(f"Trigger found: {t['name']}")
