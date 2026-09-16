import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders
from dashboard.erp_connector import query

data = get_orders('isci')
print('ORDERS IN DASHBOARD FOR JUNE 18:')
for c in data['companies']:
    for o in c['orders']:
        if '06-18' in str(o['raw_tarix']) or '05-08' in str(o['raw_tarix']):
            pass # print(c['name'].encode('ascii','ignore').decode(), o['id'], str(o['miqdar']).encode('ascii','ignore').decode(), o['cesid'].encode('ascii','ignore').decode())

sql = """
SELECT s.sen_no, e.miqdar, g.name, c.name as cname, s.tarix
FROM sm_sif_sened s
JOIN sm_sif_sened_el e ON s.idn = e.es_no
JOIN sm_goods g ON e.mal = g.idn
JOIN sm_kontra c ON s.kontra = c.idn
WHERE s.tarix >= '2026-06-18' AND s.tarix < '2026-06-19'
"""
rows = query(sql)
print('\nORDERS IN DB FOR JUNE 18:')
for r in rows:
    try:
        print((r['cname'] or '').encode('ascii','ignore').decode(), r['sen_no'], r['miqdar'], r['name'].encode('ascii','ignore').decode())
    except:
        pass
