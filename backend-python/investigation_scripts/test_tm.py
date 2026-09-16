import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import query

sql = """
SELECT DISTINCT g.idn, g.name, g.class
FROM sm_sif_sened s 
JOIN sm_sif_sened_el e ON s.idn = e.es_no 
JOIN sm_goods g ON e.mal = g.idn 
JOIN sm_kontra k ON s.kontra = k.idn 
WHERE k.name LIKE '%KURORT%' AND s.tarix >= '2026-06-18'
"""
rows = query(sql)
for r in rows:
    print(r['idn'], r['name'].encode('ascii', 'ignore').decode(), r['class'])
