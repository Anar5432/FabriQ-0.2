import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query

sql = """
    SELECT
        s.idn AS order_id,
        s.sen_no,
        s.kontra AS company_id,
        c.name AS company_name
    FROM sm_sifaris_form s WITH (NOLOCK)
    LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
    WHERE s.idn IN (1863, 2675)
    
    UNION ALL
    
    SELECT
        s.idn AS order_id,
        s.sen_no,
        s.kontra AS company_id,
        c.name AS company_name
    FROM sm_sif_sened s WITH (NOLOCK)
    LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
    WHERE s.idn IN (1863, 2675)
"""
res = query(sql)
print("Orders 1863 and 2675 base query:")
for r in res:
    print(r)
