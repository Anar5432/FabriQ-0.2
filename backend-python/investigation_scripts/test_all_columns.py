import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query

sql = """
    SELECT *
    FROM sm_sifaris_form WITH (NOLOCK)
    WHERE idn = 2675
"""
res = query(sql)
print("Columns in sm_sifaris_form for 2675:")
if res:
    for k, v in res[0].items():
        if v:
            print(f"{k}: {v}")

sql2 = """
    SELECT *
    FROM sm_sif_sened WITH (NOLOCK)
    WHERE idn = 1863
"""
res2 = query(sql2)
print("\\nColumns in sm_sif_sened for 1863:")
if res2:
    for k, v in res2[0].items():
        if v:
            print(f"{k}: {v}")

