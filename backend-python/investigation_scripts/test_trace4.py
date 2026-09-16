import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_sector_rules, query

sector = 'isci'
rules = get_sector_rules(sector)
cls_cond = rules['class_condition']
sql = f"""
        SET NOCOUNT ON;
        SELECT
            c.name AS company_name,
            g.name AS product_name
        FROM sm_sifaris_form s WITH (NOLOCK)
        JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
        LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
        JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
        WHERE {cls_cond}
          AND s.tarix >= DATEADD(DAY, -60, GETDATE())
"""
base_lines = query(sql)

bakus = [l for l in base_lines if l['company_name'] and 'BAKU' in l['company_name'].upper()]
for b in bakus:
    pn = b['product_name']
    if '(RVANA)' in pn.encode('ascii','ignore').decode():
        print(pn.encode('ascii','ignore').decode(), '->', [ord(c) for c in pn])
