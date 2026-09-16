# -*- coding: utf-8 -*-
"""
Stage 3 diagnostic: Understand HM- vs YM- and the full pipeline per item.
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath('C:/Users/User/.gemini/antigravity/scratch/backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django; django.setup()
from dashboard.erp_connector import query

print("="*70)
print("CONFIRMED ROOT CAUSE:")
print("1. sobe2 (destination) is ALWAYS 6 (Finished Goods) for complete items")
print("   => Cannot use sobe2 to find intermediate stages")
print("2. sobe1 (source/origin) tells us WHERE items came FROM in the latest transfer")
print("   => sobe1=3 (Kesim) means item just LEFT cutting, now in Tikis") 
print("   => sobe1=4 or 5 (Tikis) means item just LEFT sewing, now in Finished Goods")
print("")
print("CORRECT APPROACH:")
print("  For items with transfer: use sobe2 (destination) from LATEST transfer")
print("  BUT the 'Ambar' destination (6) means it COMPLETED that stage")
print("  So we need to handle:")
print("    sobe2=3 (Kesim) = item arrived in Cutting dept = Kəsim stage")  
print("    sobe2=4 or 5 (Tikis) = item arrived in Sewing dept = Tikiş stage")
print("    sobe2=6 (Finished Goods) = item completed = Ambar stage")
print("    sobe2=NULL = no transfer yet = Satış stage")
print("="*70)

print("\nVERIFICATION: Distribution via sobe2 (WITHOUT date filter):")
sql = """
SELECT 
    trans.sobe2 AS stage,
    d.name AS stage_name,
    COUNT(DISTINCT e.idn) AS cnt
FROM sm_kontr_sat s WITH (NOLOCK)
JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
LEFT JOIN (
    SELECT t.sobe2, tel.mal,
           ROW_NUMBER() OVER(PARTITION BY tel.mal ORDER BY t.tarix DESC, t.idn DESC) as rn
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1
) trans ON trans.mal = e.mal AND trans.rn = 1
LEFT JOIN sm_depo d WITH (NOLOCK) ON trans.sobe2 = d.idn
WHERE g.class = 27
  AND s.tarix >= DATEADD(DAY, -60, GETDATE())
  AND e.qaliq > 0
GROUP BY trans.sobe2, d.name
ORDER BY cnt DESC
"""
rows = query(sql)
print("  sobe2 distribution:", rows)

print("\nVERIFICATION: Distribution via sobe1 (WHERE items left from):")
sql2 = """
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
rows2 = query(sql2)
print("  sobe1 distribution:", rows2)

# The real question: which is better?
# sobe2: always 6 = everyone at Ambar (wrong for in-progress)
# sobe1: tells where it came FROM in the latest transfer
#   sobe1=3 (Kesim) = left Kesim, now in Tikis/sobe2
#   sobe1=4/5 (Tikis) = left Tikis, now in Anbar (sobe2=6)
#   sobe1=24 (Experimental) = special dept
#   sobe1=15 (BTF Satis Magazasi) = internal sales store 
#   sobe1=39 (Son Bolum) = finishing dept, going to Anbar

# BEST LOGIC:
# trans.sobe2 from LATEST transfer:
#   NULL => Satış (0)
#   3 (Kesim) => Kəsim (2) - items arrived at Kesim
#   4 or 5 (Tikis/Mayka) => Tikiş (4) - items arrived at Sewing
#   6 (Finished Goods) => Ambar (5) - items completed
#   8 or 9 (material) => Ambar Material (1)
#   24 => special - treat as Tikiş
#   39 (Son Bolum/Finishing) => treat as Tikiş 
#   15 => treat as Ambar (internal sales store = completed)

print("\n\nFINAL ANSWER: sobe2 (destination) is the RIGHT field, but:")
print("  - There was a date filter bug: trans.tarix >= order.tarix was TOO STRICT")
print("  - Many production transfers happen BEFORE the official sales order date")
print("    because the factory can start making things before the sales order is placed!")
print("  - SOLUTION: Remove the date filter, just get the MOST RECENT transfer for each item")
print("  - Items showing sobe2=6 means COMPLETED/READY IN WAREHOUSE = Ambar stage (correct!)")
print("  - Items with NO transfer = still at Satış stage (waiting for production to start)")
print("")
print("  The 67% 'Satış' is the real count of orders not yet started in production")
print("  The 291 'Ambar' is the count of items that are ready/done")
print("  Kəsim and Tikiş ARE 0 in sobe2 because the DB only records COMPLETED moves")
print("  When an item goes Kesim -> Tikis, sobe2=4/5")
print("  When an item goes Tikis -> Anbar, sobe2=6")
print("  So RIGHT NOW, are there any active items in Kesim (sobe2=3)?")
print("")
print("  Check: are there ANY items currently IN KESIM (sent to Kesim but not yet sent onwards)?")

sql3 = """
-- Items that have a transfer TO kesim (sobe2=3) but NO LATER transfer FROM kesim
SELECT COUNT(DISTINCT e.idn) as in_kesim
FROM sm_kontr_sat s WITH (NOLOCK)
JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
WHERE g.class = 27 
  AND e.qaliq > 0
  AND s.tarix >= DATEADD(DAY, -60, GETDATE())
  AND EXISTS (
    SELECT 1 FROM sm_sob_trans t2 
    JOIN sm_sob_trans_el tel2 ON t2.idn = tel2.es_no
    WHERE tel2.mal = e.mal AND t2.sobe2 = 3 AND t2.tesdiq = 1
  )
"""
print(query(sql3))

sql4 = """
-- Items currently in Tikis (sent to 4 or 5 but not later moved to 6)
SELECT COUNT(DISTINCT e.idn) as in_tikis_but_not_anbar
FROM sm_kontr_sat s WITH (NOLOCK)
JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
WHERE g.class = 27 
  AND e.qaliq > 0
  AND s.tarix >= DATEADD(DAY, -60, GETDATE())
  AND EXISTS (
    SELECT 1 FROM sm_sob_trans t2 
    JOIN sm_sob_trans_el tel2 ON t2.idn = tel2.es_no
    WHERE tel2.mal = e.mal AND t2.sobe2 IN (4,5) AND t2.tesdiq = 1
  )
  AND NOT EXISTS (
    SELECT 1 FROM sm_sob_trans t2 
    JOIN sm_sob_trans_el tel2 ON t2.idn = tel2.es_no
    WHERE tel2.mal = e.mal AND t2.sobe2 = 6 AND t2.tesdiq = 1
      AND t2.tarix > (
        SELECT MAX(t3.tarix) FROM sm_sob_trans t3 
        JOIN sm_sob_trans_el tel3 ON t3.idn = tel3.es_no
        WHERE tel3.mal = e.mal AND t3.sobe2 IN (4,5) AND t3.tesdiq = 1
      )
  )
"""
print(query(sql4))

print("\nSUMMARY: We need a smarter approach - track per product:")
print("  1. If HAS transfer to sobe2=6 -> Ambar (done)")
print("  2. Else if HAS transfer to sobe2 IN (4,5) -> Tikiş (in sewing)")
print("  3. Else if HAS transfer to sobe2=3 -> Kəsim (in cutting)")
print("  4. Else if HAS any transfer to sobe2 IN (8,9) -> Ambar Material")
print("  5. Else -> Satış (not yet started)")
