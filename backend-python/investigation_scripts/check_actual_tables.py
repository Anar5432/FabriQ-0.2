import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.erp_connector import query

sql = """
SELECT g.name as Cesid, s.tarix, c.name as Musteri
FROM sm_sifaris_form s
JOIN sm_sifaris_form_el e ON e.es_no = s.idn
JOIN sm_goods g ON e.mal = g.idn
LEFT JOIN sm_kontra c ON s.kontra = c.idn
WHERE UPPER(g.name) LIKE '%XURMAYI%' OR UPPER(g.name) LIKE '%AYAQ%' OR UPPER(g.name) LIKE '%50X90%'
"""
print('sm_sifaris_form:')
for r in query(sql):
    print(r)

sql2 = """
SELECT g.name as Cesid, s.tarix, c.name as Musteri
FROM sm_sif_sened s
JOIN sm_sif_sened_el e ON e.es_no = s.idn
JOIN sm_goods g ON e.mal = g.idn
LEFT JOIN sm_kontra c ON s.kontra = c.idn
WHERE UPPER(g.name) LIKE '%XURMAYI%' OR UPPER(g.name) LIKE '%AYAQ%' OR UPPER(g.name) LIKE '%50X90%'
"""
print('sm_sif_sened:')
for r in query(sql2):
    print(r)

sql3 = """
SELECT g.name as Cesid, s.tarix, s.kontra_name as Musteri
FROM sm_kontr_sat s
JOIN sm_kontr_sat_el e ON e.es_no = s.idn
JOIN sm_goods g ON e.mal = g.idn
WHERE UPPER(g.name) LIKE '%XURMAYI%' OR UPPER(g.name) LIKE '%AYAQ%' OR UPPER(g.name) LIKE '%50X90%'
"""
print('sm_kontr_sat:')
for r in query(sql3):
    print(r)
