import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query

sql = """
    SELECT 
        e.idn, 
        e.es_no, 
        g.name, 
        e.miqdar, 
        e.sat_miq,
        s.status
    FROM sm_sif_sened s WITH (NOLOCK)
    JOIN sm_sif_sened_el e WITH (NOLOCK) ON s.idn = e.es_no
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    WHERE s.idn = 4214
"""
res = query(sql)
for r in res:
    print(r)
