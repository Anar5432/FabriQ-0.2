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
            s.idn AS order_id,
            s.sen_no,
            s.yekun AS order_total,
            CONVERT(VARCHAR(10), s.tarix, 23) AS tarix,
            s.kontra AS company_id,
            c.name AS company_name,
            e.idn AS line_id,
            e.num AS line_num,
            g.idn AS product_id,
            g.name AS product_name,
            e.miqdar AS qty_ordered,
            e.miqdar AS qty_remaining
        FROM sm_sifaris_form s WITH (NOLOCK)
        JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
        LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
        JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
        WHERE {cls_cond}
          AND s.tarix >= DATEADD(DAY, -60, GETDATE())
"""
base_lines = query(sql)
print('Total:', len(base_lines))

bakus = [l for l in base_lines if l['company_name'] and 'BAKU' in l['company_name'].upper()]
for b in bakus:
    pn = b['product_name']
    print('Baku product:', pn.encode('ascii','ignore').decode())
    if 'RVANA' in pn:
        print('  >>> RVANA MATCHED IN BAKU LOOP!')

for order in base_lines:
    pn = order['product_name']
    if pn and 'RVANA' in pn:
        print('  >>> RVANA MATCHED IN MAIN LOOP!', pn.encode('ascii','ignore').decode())
