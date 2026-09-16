import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = """
SELECT 
    'sm_sifaris_form' as source,
    s.idn AS order_id,
    s.sen_no,
    g.class,
    g.name as product_name
FROM sm_sifaris_form s WITH (NOLOCK)
JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
WHERE s.idn IN (13365, 22191)

UNION ALL

SELECT 
    'sm_sif_sened' as source,
    s.idn AS order_id,
    s.sen_no,
    g.class,
    g.name as product_name
FROM sm_sif_sened s WITH (NOLOCK)
JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
WHERE s.idn IN (2717)
"""
try:
    res = query(sql)
    for r in res:
        print(r)
except Exception as e:
    print(e)
