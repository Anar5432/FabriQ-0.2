# -*- coding: utf-8 -*-
"""
Stage 2 diagnostic: Understand the YM- mapping and all stages in the DB.
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath('C:/Users/User/.gemini/antigravity/scratch/backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django; django.setup()
from dashboard.erp_connector import query

print("="*60)
print("FINDING: Most transfers land at sobe2=6 (Finished Goods Warehouse).")
print("This is because the production pipeline is:")
print("  Material -> Kesim -> Tikis -> Finished Goods (6)")
print("And the FINAL destination is always 6.")
print("")
print("KEY INSIGHT: We should track the LAST TRANSFER FROM a sobe (source)")
print("not just the last transfer TO a destination (sobe2).")
print("OR: we should track what SOBE1 (source dept) the goods are leaving from.")
print("="*60)

print("\nCheck: what SOBE1 values appear (where items are coming FROM)?")
sql = """
SELECT 
    t.sobe1,
    d.name as dept_name,
    COUNT(*) as cnt
FROM sm_sob_trans t WITH (NOLOCK)
JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
JOIN sm_goods g WITH (NOLOCK) ON tel.mal = g.idn
LEFT JOIN sm_depo d WITH (NOLOCK) ON t.sobe1 = d.idn
WHERE g.class = 27 AND t.tesdiq = 1 
  AND t.tarix >= DATEADD(DAY, -60, GETDATE())
GROUP BY t.sobe1, d.name
ORDER BY cnt DESC
"""
rows = query(sql)
for r in rows:
    print(f"  sobe1={r['sobe1']} ({r['dept_name']}) => {r['cnt']} transfers")

print("\n")
print("="*60)
print("CORE ISSUE: The production chain is:")
print("  Kəsim Sexi (3) -> Tikis Sexi (4/5) -> BTF Anbar (6)")
print("When an item moves from Kesim to Tikis, it records sobe1=3, sobe2=4/5")
print("When it moves from Tikis to Anbar, it records sobe1=4/5, sobe2=6")
print("So the LATEST transfer always has sobe2=6 (the DESTINATION).")
print("")
print("We need to use SOBE1 from the MOST RECENT transfer to know where")
print("items CURRENTLY ARE (they just left that department).")
print("OR: use sobe2 from the 2nd-to-last transfer.")
print("="*60)

print("\nCHECK: What if we use SOBE1 (source) to track current stage?")
sql2 = """
SELECT TOP 20
    trans.sobe1 AS last_dept,
    d.name AS dept_name,
    s.idn AS order_id,
    g.name AS product,
    e.qaliq
FROM sm_kontr_sat s WITH (NOLOCK)
JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
LEFT JOIN (
    SELECT t.sobe1, t.sobe2, tel.mal, t.tarix, t.idn,
           ROW_NUMBER() OVER(PARTITION BY tel.mal ORDER BY t.tarix DESC, t.idn DESC) as rn
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1
) trans ON trans.mal = e.mal AND trans.rn = 1
LEFT JOIN sm_depo d WITH (NOLOCK) ON trans.sobe1 = d.idn
WHERE g.class = 27
  AND s.tarix >= DATEADD(DAY, -60, GETDATE())
  AND e.qaliq > 0
ORDER BY s.tarix DESC
"""
rows2 = query(sql2)
from collections import Counter
stages_found = Counter()
for r in rows2:
    stages_found[f"{r['last_dept']} ({r['dept_name']})"] += 1
    print(f"  order={r['order_id']} | prod={r['product'][:40]} | sobe1={r['last_dept']}({r['dept_name']}) | qaliq={r['qaliq']}")

print(f"\nStage distribution (via sobe1): {dict(stages_found)}")

print("\n")
print("="*60)
print("CHECK: Distribution of sobe1 values across all open class-27 orders")
sql3 = """
SELECT 
    trans.sobe1 AS stage,
    d.name AS stage_name,
    COUNT(DISTINCT e.idn) AS cnt
FROM sm_kontr_sat s WITH (NOLOCK)
JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
LEFT JOIN (
    SELECT t.sobe1, t.sobe2, tel.mal,
           ROW_NUMBER() OVER(PARTITION BY tel.mal ORDER BY t.tarix DESC, t.idn DESC) as rn
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1
) trans ON trans.mal = e.mal AND trans.rn = 1
LEFT JOIN sm_depo d WITH (NOLOCK) ON trans.sobe1 = d.idn
WHERE g.class = 27
  AND s.tarix >= DATEADD(DAY, -60, GETDATE())
  AND e.qaliq > 0
GROUP BY trans.sobe1, d.name
ORDER BY cnt DESC
"""
rows3 = query(sql3)
print(f"Stage distribution via SOBE1 (source): {rows3}")
