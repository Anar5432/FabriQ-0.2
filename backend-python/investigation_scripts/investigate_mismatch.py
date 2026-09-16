import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django; django.setup()
from dashboard.erp_connector import query

print("INVESTIGATING: Why are some delivered orders (qaliq=0) showing up in Sewing/Cutting?")

# Find examples where Sales Order qaliq = 0, but latest production transfer is Kesim or Tikis
sql = """
SELECT TOP 3
    s.idn AS order_id,
    s.sen_no AS order_no,
    s.tarix AS order_date,
    hm_goods.name AS product_name,
    e.miqdar AS qty_ordered,
    trans_inner.sobe1 AS last_transfer_from,
    trans_inner.sobe2 AS last_transfer_to,
    trans_inner.tarix AS transfer_date,
    trans_inner.ym_name
FROM sm_kontr_sat s WITH (NOLOCK)
JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods hm_goods WITH (NOLOCK) ON e.mal = hm_goods.idn
JOIN (
    -- Match HM- sales items to their YM- production counterparts
    SELECT sobe1, sobe2, tarix, hm_mal, ym_name
    FROM (
        SELECT trans_inner.sobe1, trans_inner.sobe2, trans_inner.tarix, hm_goods.idn AS hm_mal, trans_inner.ym_name,
               ROW_NUMBER() OVER(PARTITION BY hm_goods.idn ORDER BY trans_inner.rn) AS match_rn
        FROM (
            SELECT t.sobe1, t.sobe2, t.tarix, tel.mal AS ym_mal, ym_g.name AS ym_name,
                   ROW_NUMBER() OVER(PARTITION BY tel.mal ORDER BY t.tarix DESC, t.idn DESC) as rn
            FROM sm_sob_trans t WITH (NOLOCK)
            JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
            JOIN sm_goods ym_g WITH (NOLOCK) ON tel.mal = ym_g.idn
            WHERE t.tesdiq = 1 AND ym_g.class = 27
        ) trans_inner
        JOIN sm_goods ym_g WITH (NOLOCK) ON trans_inner.ym_mal = ym_g.idn
        JOIN sm_goods hm_goods WITH (NOLOCK) ON 
            hm_goods.class = 27
            AND (
                hm_goods.idn = trans_inner.ym_mal
                OR
                (ym_g.name LIKE 'YM-%' AND hm_goods.name LIKE 'HM-%'
                 AND SUBSTRING(ym_g.name, 4, LEN(ym_g.name)) = SUBSTRING(hm_goods.name, 4, LEN(hm_goods.name)))
            )
        WHERE trans_inner.rn = 1
    ) deduped
    WHERE match_rn = 1
) trans_inner ON trans_inner.hm_mal = e.mal
WHERE hm_goods.class = 27
  AND s.tarix >= DATEADD(DAY, -60, GETDATE())
  AND e.qaliq = 0
  AND trans_inner.sobe1 IN (3, 4, 5) -- 3=Kesim, 4/5=Tikis
ORDER BY s.tarix DESC
"""

rows = query(sql)
for r in rows:
    print(f"\nOrder {r['order_id']} ({r['order_no']}) Date: {r['order_date']}")
    print(f"Product: {r['product_name']}")
    print(f"Ordered: {r['qty_ordered']}  |  Qaliq: 0 (Delivered)")
    print(f"LATEST TRANSFER found in DB for this product: {r['ym_name']}")
    print(f"Transfer Date: {r['transfer_date']} | From Sobe {r['last_transfer_from']} to {r['last_transfer_to']}")
