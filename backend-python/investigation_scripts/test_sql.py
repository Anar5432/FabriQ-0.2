import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.erp_connector import query

sql = """
SELECT s.idn AS order_id, s.sen_no, s.tarix, c.name AS company_name, g.name AS product_name, e.miqdar, e.sat_miq
FROM sm_sif_sened s WITH (NOLOCK)
JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
WHERE UPPER(g.name) LIKE '%XURMAYI%' OR UPPER(g.name) LIKE '%AYAQ%' OR UPPER(g.name) LIKE '%50X90%'
"""
rows = query(sql)
print('Count:', len(rows))
for r in rows[:10]:
    name = r['product_name'].encode('ascii', 'replace').decode()
    comp = r['company_name']
    if comp:
        comp = comp.encode('ascii', 'replace').decode()
    print(r['tarix'], comp, name, r['miqdar'], r['sat_miq'])
