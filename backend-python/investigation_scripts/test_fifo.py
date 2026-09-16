import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django; django.setup()
from dashboard.erp_connector import query

cls = '(27)'
print("Step 1: Get orders")
sql = f"""
SET NOCOUNT ON;
SELECT
    s.idn AS order_id,
    CONVERT(VARCHAR(10), s.tarix, 23) AS tarix,
    s.kontra_name AS company_name,
    g.idn AS product_id,
    g.name AS product_name,
    e.miqdar AS qty_ordered,
    e.qaliq AS qty_remaining
FROM sm_kontr_sat s WITH (NOLOCK)
JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
WHERE g.class IN {cls}
  AND s.tarix >= DATEADD(DAY, -60, GETDATE())
ORDER BY s.tarix ASC;
"""
orders = query(sql)
print(f"Orders found: {len(orders)}")

print("Step 2: Get balances")
sql_balances = f"""
SELECT 
    hm_goods.idn AS hm_mal,
    dept.idn AS dept_id,
    ISNULL(ins.qty_in, 0) - ISNULL(outs.qty_out, 0) AS balance
FROM sm_goods hm_goods WITH (NOLOCK)
JOIN sm_goods ym_g WITH (NOLOCK) ON 
    ym_g.class IN {cls} AND (
        hm_goods.idn = ym_g.idn
        OR (ym_g.name LIKE 'YM-%' AND hm_goods.name LIKE 'HM-%'
            AND SUBSTRING(ym_g.name, 4, LEN(ym_g.name)) = SUBSTRING(hm_goods.name, 4, LEN(hm_goods.name)))
    )
JOIN (
    SELECT t.sobe2 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_in
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1
    GROUP BY t.sobe2, tel.mal
) ins ON ym_g.idn = ins.mal
LEFT JOIN sm_depo dept WITH (NOLOCK) ON ins.dept_id = dept.idn
LEFT JOIN (
    SELECT t.sobe1 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_out
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1 AND t.sobe1 IS NOT NULL
    GROUP BY t.sobe1, tel.mal
) outs ON ins.dept_id = outs.dept_id AND ins.mal = outs.mal
WHERE hm_goods.class IN {cls}
  AND (ISNULL(ins.qty_in, 0) - ISNULL(outs.qty_out, 0)) > 0
"""
balances = query(sql_balances)
print(f"Balances found: {len(balances)}")

from collections import defaultdict
import copy

product_balances = defaultdict(lambda: defaultdict(float))
for b in balances:
    product_balances[b['hm_mal']][b['dept_id']] += float(b['balance'])

# FIFO logic
processed_orders = []

for order in orders:
    qaliq = float(order['qty_remaining'] or 0)
    ordered = float(order['qty_ordered'] or 0)
    delivered = ordered - qaliq
    
    if delivered > 0:
        o_deliv = copy.deepcopy(order)
        o_deliv['split_qty'] = delivered
        o_deliv['phase'] = 6 # Anbar/Tamamlandı
        processed_orders.append(o_deliv)
        
    if qaliq == 0:
        continue
        
    hm_mal = order['product_id']
    bals = product_balances[hm_mal]
    
    # Priority order of departments to pull from (closest to finish first)
    # 6=Anbar, 15=Internal Sales, 39=Son Bolum, 5=Mayka, 4=Tikis, 3=Kesim, 24=Experimental, 8/9=Material
    dept_priority = [6, 15, 39, 5, 4, 3, 24, 8, 9]
    
    remaining_to_find = qaliq
    
    for dept_id in dept_priority:
        if remaining_to_find <= 0:
            break
        available = bals[dept_id]
        if available > 0:
            take = min(available, remaining_to_find)
            bals[dept_id] -= take
            remaining_to_find -= take
            
            o_split = copy.deepcopy(order)
            o_split['split_qty'] = take
            o_split['phase'] = dept_id
            processed_orders.append(o_split)
            
    # If there's still remaining_to_find, they are at stage 0 (Satış)
    if remaining_to_find > 0:
        o_split = copy.deepcopy(order)
        o_split['split_qty'] = remaining_to_find
        o_split['phase'] = 0
        processed_orders.append(o_split)

print(f"Total split order lines: {len(processed_orders)}")
for o in processed_orders[:10]:
    print(f"Order {o['order_id']} | {o['product_name'][:30]} | split={o['split_qty']}/{o['qty_ordered']} | phase={o['phase']}")
