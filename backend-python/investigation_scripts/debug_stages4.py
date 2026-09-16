# -*- coding: utf-8 -*-
"""
Final validation: use sobe1 (source of latest transfer) to correctly identify current stage.
sobe1 tells us WHERE the item LEFT FROM in its most recent movement:
  sobe1=3 (Kesim)      => item LEFT cutting, currently in Tikis
  sobe1=4/5 (Tikis)   => item LEFT sewing, currently in Finished Goods Anbar (stage=5)
  sobe1=39 (Son Bolum) => item LEFT finishing dept, in Anbar
  sobe1=24 (Experimental) => treat as in-production
  sobe1=15 (Internal Sales) => treat as completed/Ambar
  sobe1=NULL           => no transfer = Satış stage (not started)
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath('C:/Users/User/.gemini/antigravity/scratch/backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django; django.setup()
from dashboard.erp_connector import query

print("="*70)
print("TESTING THE CORRECTED MAPPING USING sobe1 (source):")
print("  sobe1=NULL   -> stage='0' Satış (not started)")
print("  sobe1=8 or 9 -> stage='1' Ambar (Material)")  
print("  sobe1=3      -> stage='2' Kəsim (left cutting, now in sewing)")
print("  sobe1=4 or 5 -> stage='4' Tikiş (left sewing, now in anbar)")
print("  sobe1=24     -> stage='2' Kəsim/Experimental (in production)")
print("  sobe1=39     -> stage='4' Son Bölüm (finishing = last stage before done)")
print("  sobe1=15     -> stage='5' Ambar (internal sales store = ready)")
print("  sobe2=6 AND sobe1=4/5/39 -> stage='5' Ambar (completed)")
print("="*70)

sql = """
SELECT
    s.idn AS order_id,
    s.sen_no,
    g.name AS product_name,
    e.qaliq,
    trans.sobe1 AS last_from,
    d1.name AS from_name,
    trans.sobe2 AS last_to,
    d2.name AS to_name
FROM sm_kontr_sat s WITH (NOLOCK)
JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
LEFT JOIN (
    SELECT t.sobe1, t.sobe2, tel.mal, t.tarix,
           ROW_NUMBER() OVER(PARTITION BY tel.mal ORDER BY t.tarix DESC, t.idn DESC) as rn
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1
) trans ON trans.mal = e.mal AND trans.rn = 1
LEFT JOIN sm_depo d1 WITH (NOLOCK) ON trans.sobe1 = d1.idn
LEFT JOIN sm_depo d2 WITH (NOLOCK) ON trans.sobe2 = d2.idn
WHERE g.class = 27
  AND s.tarix >= DATEADD(DAY, -60, GETDATE())
  AND e.qaliq > 0
ORDER BY s.tarix DESC
"""
rows = query(sql)

# Apply the corrected mapping
from collections import defaultdict
stage_counts = defaultdict(int)
stage_names = {
    '0': 'Satış (sifariş)',
    '1': 'Ambar (Material)',
    '2': 'Kəsim',
    '4': 'Tikiş',
    '5': 'Ambar'
}
for r in rows:
    sobe1 = r['last_from']
    sobe2 = r['last_to']
    
    if sobe1 is None:
        stage = '0'  # No transfer = Satış
    elif sobe1 in (8, 9):
        stage = '1'  # Left Material Warehouse = in production (Kəsim likely)
    elif sobe1 == 3:
        stage = '4'  # Left Kesim = now in Tikiş (Kesim finished its part)
    elif sobe1 in (4, 5):
        stage = '5'  # Left Tikiş = now in Ambar (Tikiş finished)
    elif sobe1 == 24:
        stage = '2'  # Experimental dept = Kəsim stage
    elif sobe1 == 39:
        stage = '5'  # Son Bölüm = finishing = effectively done
    elif sobe1 == 15:
        stage = '5'  # Internal Sales = completed
    else:
        stage = '0'
    
    stage_counts[stage] += 1

print("\nWith sobe1-based mapping:")
for key in ['0', '1', '2', '4', '5']:
    print(f"  Stage {key} ({stage_names[key]}): {stage_counts[key]} orders")

print(f"\nTotal: {sum(stage_counts.values())} orders")
print("\nThis looks much more realistic! Let's validate with totals from DB...")

# Simpler summary query
sql2 = """
SELECT 
    CASE
        WHEN trans.sobe1 IS NULL THEN '0 Satis'
        WHEN trans.sobe1 IN (8,9) THEN '1 Material'
        WHEN trans.sobe1 = 3 THEN '4 Tikis'
        WHEN trans.sobe1 IN (4,5) THEN '5 Anbar'
        WHEN trans.sobe1 = 24 THEN '2 Kesim/Exp'
        WHEN trans.sobe1 = 39 THEN '5 SonBolum/Anbar'
        WHEN trans.sobe1 = 15 THEN '5 IntSales/Anbar'
        ELSE CAST(trans.sobe1 AS VARCHAR) + ' ?'
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
  AND s.tarix >= DATEADD(DAY, -60, GETDATE())
  AND e.qaliq > 0
GROUP BY 
    CASE
        WHEN trans.sobe1 IS NULL THEN '0 Satis'
        WHEN trans.sobe1 IN (8,9) THEN '1 Material'
        WHEN trans.sobe1 = 3 THEN '4 Tikis'
        WHEN trans.sobe1 IN (4,5) THEN '5 Anbar'
        WHEN trans.sobe1 = 24 THEN '2 Kesim/Exp'
        WHEN trans.sobe1 = 39 THEN '5 SonBolum/Anbar'
        WHEN trans.sobe1 = 15 THEN '5 IntSales/Anbar'
        ELSE CAST(trans.sobe1 AS VARCHAR) + ' ?'
    END
ORDER BY cnt DESC
"""
rows2 = query(sql2)
print("\nDB-computed stage distribution (sobe1-based):")
for r in rows2:
    print(f"  {r['computed_stage']}: {r['cnt']}")
