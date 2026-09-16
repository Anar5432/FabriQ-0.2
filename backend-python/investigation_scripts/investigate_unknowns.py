import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = "SELECT * FROM sm_kontra WHERE idn = 1731"
res = query(sql)
print("--- sm_kontra for 1731 ---")
if res:
    for k, v in res[0].items():
        if v and str(v).strip():
            print(f"{k}: {v}")

print("\n--- Any other tables for 1731? ---")
tables = ['sm_kontra_class', 'sm_kontra_is', 'sm_kontra_bar', 'sm_kontra_sir', 'sm_kontra_kafe', 'sm_kontra_class_el']
for t in tables:
    try:
        r = query(f"SELECT * FROM {t} WHERE kontra = 1731")
        if r: print(f"Found in {t}: {r}")
    except:
        pass
        
print("\n--- Maybe search the entire database for 'Ilqar' to see where it comes from? ---")
sql_search = """
SELECT TOP 20 'sm_kontra' as tbl, idn, name, full_name, v_name FROM sm_kontra WHERE name LIKE '%lqar%' OR full_name LIKE '%lqar%' OR v_name LIKE '%lqar%'
"""
print(query(sql_search))

