import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query, get_sector_rules

rules = get_sector_rules('underwear')
cls_cond = rules['class_condition']

sql = f"""
    SELECT
        s.idn AS order_id,
        CONVERT(VARCHAR(10), s.tarix, 23) AS tarix,
        s.kontra AS company_id,
        c.name AS company_name,
        e.idn AS line_id,
        g.idn AS product_id,
        g.name AS product_name
    FROM sm_sif_sened s WITH (NOLOCK)
    JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
    LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    WHERE {cls_cond}
      AND s.idn = 3420
"""

print("Running manual query for 3420...")
res = query(sql)
for r in res:
    print(f"product: {r['product_name']}, company_id: {r['company_id']}, company_name: '{r['company_name']}', type: {type(r['company_name'])}")
