# -*- coding: utf-8 -*-
"""
Final check: understand qaliq > 0 items - are they really 'in production' or 'waiting in warehouse'?
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath('C:/Users/User/.gemini/antigravity/scratch/backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django; django.setup()
from dashboard.erp_connector import query

print("="*70)
print("UNDERSTANDING qaliq: what does 'qaliq > 0' mean in context?")
print("qaliq = remaining quantity not yet delivered to customer")
print("An item can be in FINISHED GOODS WAREHOUSE (sobe2=6) with qaliq>0")
print("meaning it's MADE but not yet shipped/delivered to customer")
print("="*70)

# The real fix needed: items at Ambar (sobe2=6) with qaliq>0 = WAITING IN WAREHOUSE = stage 5
# Items with no transfer and qaliq>0 = NOT YET STARTED = stage 0  
# Items with sobe2=4/5 (latest) = IN TIKIS = stage 4 (but most already went to 6)
# There ARE really no items currently in Kesim or Tikis for these open orders

# Look beyond 60 days for full picture
print("\nExpanding to 180 days - are there really items in middle stages?")
sql = """
SELECT 
    CASE
        WHEN trans.sobe1 IS NULL THEN '0 Satis'
        WHEN trans.sobe1 IN (8,9) THEN '1 Material'
        WHEN trans.sobe1 = 3 THEN '4 Tikis (left kesim)'
        WHEN trans.sobe1 IN (4,5) THEN '5 Anbar (left tikis)'
        WHEN trans.sobe1 = 24 THEN '2 Exp/Kesim'
        WHEN trans.sobe1 = 39 THEN '5 SonBolum/Anbar'
        WHEN trans.sobe1 = 15 THEN '5 IntSales/Anbar'
        ELSE CAST(trans.sobe1 AS VARCHAR) + ' other'
    END AS computed_stage,
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
WHERE g.class = 27
  AND s.tarix >= DATEADD(DAY, -180, GETDATE())
  AND e.qaliq > 0
GROUP BY 
    CASE
        WHEN trans.sobe1 IS NULL THEN '0 Satis'
        WHEN trans.sobe1 IN (8,9) THEN '1 Material'
        WHEN trans.sobe1 = 3 THEN '4 Tikis (left kesim)'
        WHEN trans.sobe1 IN (4,5) THEN '5 Anbar (left tikis)'
        WHEN trans.sobe1 = 24 THEN '2 Exp/Kesim'
        WHEN trans.sobe1 = 39 THEN '5 SonBolum/Anbar'
        WHEN trans.sobe1 = 15 THEN '5 IntSales/Anbar'
        ELSE CAST(trans.sobe1 AS VARCHAR) + ' other'
    END
ORDER BY cnt DESC
"""
rows = query(sql)
print("180 days distribution:", rows)

print("\n\nACTION PLAN: The mapping should use sobe1 (source) from latest transfer:")
print("  NULL => Satış")
print("  3 => Kəsim-LEFT = now in Tikiş (stage 4)")
print("  4,5 => Tikiş-LEFT = now in Ambar (stage 5)")
print("  24 => Experimental = Kəsim (stage 2)")
print("  39 => Son Bölüm = Ambar (stage 5)")
print("  15 => Internal Sales = Ambar (stage 5)")
print("")
print("BUT WAIT - do any items show sobe1=3 (LEFT Kesim) recently?")

sql2 = """
SELECT TOP 10 g.name, t.sobe1, t.sobe2, t.tarix
FROM sm_sob_trans t 
JOIN sm_sob_trans_el tel ON t.idn = tel.es_no
JOIN sm_goods g ON tel.mal = g.idn
WHERE g.class = 27 AND t.sobe1 = 3 AND t.tesdiq = 1
ORDER BY t.tarix DESC
"""
rows2 = query(sql2)
for r in rows2:
    print(f"  sobe1=3 example: {r['name'][:50]} | sobe2={r['sobe2']} | date={r['tarix']}")
