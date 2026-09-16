import os
import sys
import django
import json

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

def default(o):
    return str(o)

sql = "SELECT * FROM sm_kontra WHERE idn = 1731"
res = query(sql)
print("sm_kontra 1731:")
print(json.dumps(res, default=default, indent=2))

sql2 = "SELECT * FROM sm_sif_sened WHERE idn = 4108"
res2 = query(sql2)
print("\nsm_sif_sened 4108:")
print(json.dumps(res2, default=default, indent=2))

sql3 = "SELECT * FROM sm_sifaris_form WHERE sifaris = 4108 OR idn = 4108"
res3 = query(sql3)
print("\nsm_sifaris_form for 4108:")
print(json.dumps(res3, default=default, indent=2))

