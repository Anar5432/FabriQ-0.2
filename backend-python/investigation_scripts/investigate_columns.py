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
for r in res:
    for k, v in r.items():
        if v and isinstance(v, str) and v.strip():
            print(k, ":", v)
