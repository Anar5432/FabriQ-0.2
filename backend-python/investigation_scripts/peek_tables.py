import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django; django.setup()
from dashboard.erp_connector import query

tables_to_check = [
    'sm_tech_plan',
    'sm_tech_plan_sif',
    'sm_maya_gun',
    'sm_xm_plan',
    'sm_esas_ves',
    'sm_ev_class'
]

for t in tables_to_check:
    print(f"\n--- Checking table {t} ---")
    try:
        sql = f"SELECT TOP 3 * FROM {t} ORDER BY idn DESC"
        rows = query(sql)
        if not rows:
            print("Table is empty.")
        else:
            for k, v in rows[0].items():
                if v is not None:
                    print(f"  {k}: {v}")
    except Exception as e:
        print(f"Error querying table: {e}")

print("\n--- Checking for Operation or Route tables ---")
sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE '%oper%' OR TABLE_NAME LIKE '%marsrut%'"
rows = query(sql)
for r in rows:
    print(r['TABLE_NAME'])

