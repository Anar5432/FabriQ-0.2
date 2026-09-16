import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import query

sql = """
SELECT 'kontr_sat' as src, s.tarix, s.idn, s.sen_no, g.name, e.miqdar
FROM sm_kontr_sat s 
JOIN sm_kontr_sat_el e ON s.idn = e.es_no 
JOIN sm_goods g ON e.mal = g.idn 
JOIN sm_kontra k ON s.kontra = k.idn 
WHERE k.name LIKE '%KURORT%' AND s.tarix >= '2026-06-18'
UNION ALL
SELECT 'sif_form' as src, s.tarix, s.idn, s.sen_no, g.name, e.miqdar
FROM sm_sifaris_form s 
JOIN sm_sifaris_form_el e ON s.idn = e.es_no 
JOIN sm_goods g ON e.mal = g.idn 
JOIN sm_kontra k ON s.kontra = k.idn 
WHERE k.name LIKE '%KURORT%' AND s.tarix >= '2026-06-18'
UNION ALL
SELECT 'sif_sened' as src, s.tarix, s.idn, s.sen_no, g.name, e.miqdar
FROM sm_sif_sened s 
JOIN sm_sif_sened_el e ON s.idn = e.es_no 
JOIN sm_goods g ON e.mal = g.idn 
JOIN sm_kontra k ON s.kontra = k.idn 
WHERE k.name LIKE '%KURORT%' AND s.tarix >= '2026-06-18'
"""
rows = query(sql)
for r in rows:
    print(r['src'], r['tarix'], r['idn'], r['sen_no'], r['name'].encode('ascii', 'ignore').decode(), r['miqdar'])
