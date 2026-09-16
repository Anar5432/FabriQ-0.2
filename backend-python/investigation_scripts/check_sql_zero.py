import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_sector_rules, query

rules = get_sector_rules('underwear')
cls_cond = rules['class_condition']
date_filter_form = "AND s.tarix >= DATEADD(YEAR, -2, GETDATE())"
date_filter_sened = "AND s.tarix >= DATEADD(YEAR, -2, GETDATE())"

sql = f"""
SELECT
    ISNULL(s.sifaris, s.idn) AS order_id,
    s.sen_no
FROM sm_sifaris_form s WITH (NOLOCK)
JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
WHERE {cls_cond}
  {date_filter_form}
"""
res = query(sql)
print(f"Total sm_sifaris_form lines: {len(res)}")

sql2 = f"""
SELECT
    s.idn AS order_id,
    s.sen_no
FROM sm_sif_sened s WITH (NOLOCK)
JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
WHERE {cls_cond}
  AND s.idn NOT IN (SELECT sifaris FROM sm_sifaris_form WHERE sifaris IS NOT NULL)
  {date_filter_sened}
"""
res2 = query(sql2)
print(f"Total sm_sif_sened lines: {len(res2)}")
