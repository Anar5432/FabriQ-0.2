import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query

sql = """
            SELECT
                s.idn AS order_id, s.sen_no, s.tam_yek AS order_total,
                CONVERT(VARCHAR(10), s.tarix, 23) AS tarix,
                s.kontra AS company_id, c.name AS company_name,
                e.idn AS line_id, e.num AS line_num, g.idn AS product_id,
                g.name AS product_name, e.miqdar AS qty_ordered, 0 AS qty_remaining,
                NULL AS parent_order_id
            FROM sm_kontr_sat s WITH (NOLOCK)
            JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
            LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
            JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
            WHERE s.idn IN (4108)
"""
res = query(sql)
print("MISSING PARENTS QUERY:")
for r in res:
    print(r)

