import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import query, get_sector_rules

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
print('FOUND ROWS:', len(base_lines))
bakus = [l for l in base_lines if l['company_name'] and 'BAKU' in l['company_name'].upper()]
print('BAKUS:', len(bakus))
if len(bakus) > 0:
    for b in bakus:
        print(b['product_name'].encode('ascii','ignore').decode())
