# -*- coding: utf-8 -*-
"""
Validate stage data - show sample orders at each stage
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath('C:/Users/User/.gemini/antigravity/scratch/backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django; django.setup()
from dashboard.erp_connector import query

print("VALIDATION: Sample orders per stage (sobe1-based)")

sql = """
SELECT
    s.idn AS order_id,
    s.sen_no,
    g.name AS product_name,
    e.qaliq,
    trans.sobe1 AS last_from,
    d1.name AS from_name,
    CASE
        WHEN trans.sobe1 IS NULL OR trans.sobe1 = 0 THEN '0 Satis'
        WHEN trans.sobe1 IN (8,9) THEN '1 Anbar Material'
        WHEN trans.sobe1 = 24 THEN '2 Kesim'
        WHEN trans.sobe1 = 3 THEN '4 Tikis (left Kesim)'
        WHEN trans.sobe1 IN (4,5,39) THEN '5 Anbar (left Tikis)'
        WHEN trans.sobe1 IN (6,15) THEN '5 Anbar (done)'
        ELSE CAST(trans.sobe1 AS VARCHAR) + ' other'
    END AS stage_label
FROM sm_kontr_sat s WITH (NOLOCK)
JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
LEFT JOIN (
    SELECT trans_inner.sobe1, trans_inner.sobe2, hm_goods.idn AS hm_mal
    FROM (
        SELECT t.sobe1, t.sobe2, tel.mal AS ym_mal,
               ROW_NUMBER() OVER(PARTITION BY tel.mal ORDER BY t.tarix DESC, t.idn DESC) as rn
        FROM sm_sob_trans t WITH (NOLOCK)
        JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
        JOIN sm_goods ym_g WITH (NOLOCK) ON tel.mal = ym_g.idn
        WHERE t.tesdiq = 1
          AND ym_g.class IN (27)
    ) trans_inner
    JOIN sm_goods ym_g WITH (NOLOCK) ON trans_inner.ym_mal = ym_g.idn
    JOIN sm_goods hm_goods WITH (NOLOCK) ON 
        hm_goods.class IN (27)
        AND (
            hm_goods.idn = trans_inner.ym_mal
            OR
            (ym_g.name LIKE 'YM-%' AND hm_goods.name LIKE 'HM-%'
             AND SUBSTRING(ym_g.name, 4, LEN(ym_g.name)) = SUBSTRING(hm_goods.name, 4, LEN(hm_goods.name)))
        )
    WHERE trans_inner.rn = 1
) trans ON trans.hm_mal = e.mal
LEFT JOIN sm_depo d1 WITH (NOLOCK) ON trans.sobe1 = d1.idn
WHERE g.class = 27
  AND s.tarix >= DATEADD(DAY, -60, GETDATE())
  AND e.qaliq > 0
ORDER BY stage_label, s.tarix DESC
"""
rows = query(sql)

from collections import defaultdict
by_stage = defaultdict(list)
for r in rows:
    by_stage[r['stage_label']].append(r)

for stage, items in sorted(by_stage.items()):
    print(f"\n--- Stage: {stage} ({len(items)} items) ---")
    for r in items[:3]:
        print(f"  order={r['order_id']} | {r['product_name'][:50]} | sobe1={r['last_from']}({r['from_name']}) | qaliq={r['qaliq']}")
    if len(items) > 3:
        print(f"  ... and {len(items)-3} more")
