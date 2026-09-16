import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query

sql = """
    SELECT idn, name
    FROM sm_kontra WITH (NOLOCK)
    WHERE idn IN (840, 905)
"""
res = query(sql)
print("sm_kontra details:")
for r in res:
    print(r)
