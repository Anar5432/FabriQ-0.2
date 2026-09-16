import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.erp_connector import query

sql = "SELECT s.idn, s.sen_no, s.tarix, g.name, g.class, e.miqdar, e.sat_miq FROM sm_sif_sened s JOIN sm_sif_sened_el e ON e.es_no = s.idn JOIN sm_goods g ON e.mal = g.idn WHERE s.sen_no = '004181' OR s.idn = 4181"
rows = query(sql)
for r in rows:
    print(r['idn'], r['sen_no'], r['tarix'], r['miqdar'], r['sat_miq'], r['class'], r['name'].encode('ascii', 'ignore').decode())
