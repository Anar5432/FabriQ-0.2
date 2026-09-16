import os
import sys
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()

from dashboard.erp_connector import get_connection

tables_to_check = [
    'sm_smeta_xerc',
    'sm_sifaris_form',
    'users_group_oper',
    'sm_tech_plan_cem_xammal',
    'sm_tech_plan_xammal',
    'sm_xm_plan_sif',
    'users_group_report',
    'sm_tech_plan'
]

query = """
SELECT 
    c.name AS ColumnName,
    ty.name AS DataType,
    c.column_id
FROM sys.columns c
JOIN sys.types ty ON c.user_type_id = ty.user_type_id
WHERE c.object_id = OBJECT_ID(%s)
ORDER BY c.column_id DESC
"""

conn = get_connection()
cursor = conn.cursor(as_dict=True)

print("--- ANALYZING LIKELY ADDED COLUMNS (HIGHEST COLUMN IDs) ---")
for t in tables_to_check:
    cursor.execute(query, (t,))
    cols = cursor.fetchall()
    print(f"\nTable: {t}")
    # Print the last 5 columns added to this table
    for i, c in enumerate(cols[:5]):
        print(f"  {c['column_id']}: {c['ColumnName']} ({c['DataType']})")
