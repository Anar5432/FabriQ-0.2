# -*- coding: utf-8 -*-
"""
Deep diagnostic: find out why isci orders show only in stage 0 or 5.
This script will print raw DB data to understand the transfer linkage.
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath('C:/Users/User/.gemini/antigravity/scratch/backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django; django.setup()
from dashboard.erp_connector import query

print("=" * 60)
print("STEP 1: What's in sm_sob_trans for class 27 recently?")
print("=" * 60)
sql = """
SELECT TOP 30
    t.idn as trans_id,
    t.sobe1, d1.name as from_name,
    t.sobe2, d2.name as to_name,
    t.tesdiq,
    t.tarix,
    g.name as item_name,
    g.class,
    tel.miqdar
FROM sm_sob_trans t WITH (NOLOCK)
JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
JOIN sm_goods g WITH (NOLOCK) ON tel.mal = g.idn
LEFT JOIN sm_depo d1 WITH (NOLOCK) ON t.sobe1 = d1.idn
LEFT JOIN sm_depo d2 WITH (NOLOCK) ON t.sobe2 = d2.idn
WHERE g.class = 27 AND t.tesdiq = 1
ORDER BY t.tarix DESC, t.idn DESC
"""
rows = query(sql)
if rows:
    for r in rows:
        print(f"  trans={r['trans_id']} | from={r['sobe1']}({r['from_name']}) -> to={r['sobe2']}({r['to_name']}) | date={r['tarix']} | item={r['item_name'][:50]}")
else:
    print("  NO DATA!")

print()
print("=" * 60)
print("STEP 2: Open class-27 orders (last 60 days) vs their transfers")
print("=" * 60)
sql2 = """
SELECT TOP 20
    s.idn AS order_id,
    s.sen_no,
    s.tarix AS order_date,
    g.name AS product_name,
    e.qaliq,
    trans.sobe2 AS stage,
    d.name AS stage_name,
    trans.tarix AS trans_date,
    trans.rn
FROM sm_kontr_sat s WITH (NOLOCK)
JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
LEFT JOIN (
    SELECT t.sobe2, tel.mal, t.tarix, t.idn,
           ROW_NUMBER() OVER(PARTITION BY tel.mal ORDER BY t.tarix DESC, t.idn DESC) as rn
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1
) trans ON trans.mal = e.mal AND trans.rn = 1
LEFT JOIN sm_depo d WITH (NOLOCK) ON trans.sobe2 = d.idn
WHERE g.class = 27
  AND s.tarix >= DATEADD(DAY, -60, GETDATE())
  AND e.qaliq > 0
ORDER BY s.tarix DESC
"""
rows2 = query(sql2)
if rows2:
    for r in rows2:
        print(f"  order={r['order_id']} | date={r['order_date']} | prod={r['product_name'][:40]} | qaliq={r['qaliq']} | stage={r['stage']}({r['stage_name']}) | trans_date={r['trans_date']}")
else:
    print("  NO DATA!")

print()
print("=" * 60)
print("STEP 3: How many items match the date filter (trans.tarix >= order.tarix)?")
print("=" * 60)
sql3 = """
SELECT 
    COUNT(DISTINCT e.idn) as total_open_lines,
    SUM(CASE WHEN trans.sobe2 IS NOT NULL THEN 1 ELSE 0 END) as lines_with_stage,
    SUM(CASE WHEN trans.sobe2 IS NULL THEN 1 ELSE 0 END) as lines_without_stage
FROM sm_kontr_sat s WITH (NOLOCK)
JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
LEFT JOIN (
    SELECT t.sobe2, tel.mal, t.tarix,
           ROW_NUMBER() OVER(PARTITION BY tel.mal ORDER BY t.tarix DESC, t.idn DESC) as rn
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1
) trans ON trans.mal = e.mal AND trans.rn = 1 AND trans.tarix >= CAST(s.tarix AS DATE)
WHERE g.class = 27
  AND s.tarix >= DATEADD(DAY, -60, GETDATE())
  AND e.qaliq > 0
"""
rows3 = query(sql3)
print(f"  {rows3}")

print()
print("=" * 60)
print("STEP 4: WITHOUT the date filter - how many items match?")
print("=" * 60)
sql4 = """
SELECT 
    COUNT(DISTINCT e.idn) as total_open_lines,
    SUM(CASE WHEN trans.sobe2 IS NOT NULL THEN 1 ELSE 0 END) as lines_with_stage,
    SUM(CASE WHEN trans.sobe2 IS NULL THEN 1 ELSE 0 END) as lines_without_stage
FROM sm_kontr_sat s WITH (NOLOCK)
JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
LEFT JOIN (
    SELECT t.sobe2, tel.mal, t.tarix,
           ROW_NUMBER() OVER(PARTITION BY tel.mal ORDER BY t.tarix DESC, t.idn DESC) as rn
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1
) trans ON trans.mal = e.mal AND trans.rn = 1
WHERE g.class = 27
  AND s.tarix >= DATEADD(DAY, -60, GETDATE())
  AND e.qaliq > 0
"""
rows4 = query(sql4)
print(f"  {rows4}")

print()
print("=" * 60)
print("STEP 5: Sample stage distribution WITHOUT date filter")
print("=" * 60)
sql5 = """
SELECT 
    trans.sobe2 AS stage,
    d.name AS stage_name,
    COUNT(DISTINCT e.idn) AS cnt
FROM sm_kontr_sat s WITH (NOLOCK)
JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
LEFT JOIN (
    SELECT t.sobe2, tel.mal, t.tarix,
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
rows5 = query(sql5)
print(f"  Stage distribution: {rows5}")
