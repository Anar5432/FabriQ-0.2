import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.erp_connector import query

rows = query("SELECT t.sen_no, tel.mal as idn, g.name, g.class FROM sm_sifaris t JOIN sm_sifaris_el tel ON t.idn = tel.es_no JOIN sm_goods g ON tel.mal = g.idn WHERE t.idn = 4181")
for r in rows:
    print(r['sen_no'], r['idn'], str(r['name'].encode('ascii', 'ignore')), r['class'])

