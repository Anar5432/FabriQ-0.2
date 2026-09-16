import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_sector_rules
from dashboard.erp_connector import query

sector = 'isci'
rules = get_sector_rules(sector)
cls_cond = rules['class_condition']
sql_pending = f"""
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
            (e.miqdar - ISNULL(e.sat_miq, 0)) AS qty_remaining,
            0 AS current_phase,
            '' AS phase_name
        FROM sm_sif_sened s WITH (NOLOCK)
        JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
        LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
        JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
        WHERE {cls_cond}
          AND ((e.miqdar - ISNULL(e.sat_miq, 0)) > 0 OR s.tarix >= DATEADD(DAY, -60, GETDATE()))
"""
rows = query(sql_pending)
found = 0
for r in rows:
    if r['sen_no'] == '004181':
        found += 1
print('Found 004181 in sql_pending query directly:', found)
