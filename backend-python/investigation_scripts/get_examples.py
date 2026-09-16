import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

sql = '''
SELECT TOP 2 s.sen_no, g.name, sm.idn as smeta_id
FROM sm_sifaris_form s WITH (NOLOCK)
JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
JOIN sm_smeta_satis ss WITH (NOLOCK) ON ss.mal = g.idn
JOIN sm_smeta sm WITH (NOLOCK) ON sm.idn = ss.es_no
WHERE sm.tesdiq = 1
  AND NOT EXISTS (SELECT 1 FROM sm_smeta_xerc sx WITH (NOLOCK) WHERE sx.es_no = sm.idn)
'''
res = query(sql)
for r in res:
    print(f"Order: {r['sen_no']} - Product: {r['name']} - SMETA ID: {r['smeta_id']}")
