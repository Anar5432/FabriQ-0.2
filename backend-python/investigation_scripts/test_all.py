import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.erp_connector import query

for table in ['sm_sifaris', 'sm_sifaris_form', 'sm_sif_sened', 'sm_kontr_sat']:
    try:
        rows = query(f"SELECT t.sen_no, t.idn, tel.mal as p_id, g.name FROM {table} t JOIN {table}_el tel ON t.idn = tel.es_no JOIN sm_goods g ON tel.mal = g.idn WHERE g.name LIKE '%09/0018%'")
        for r in rows:
            print(f"{table}: sen_no={r['sen_no']} idn={r['idn']} name={r['name'].encode('ascii', 'ignore')}")
    except Exception as e:
        print(e)

