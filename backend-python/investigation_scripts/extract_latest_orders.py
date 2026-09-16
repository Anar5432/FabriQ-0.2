import os
import sys
import django
import json

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

results = {}

# 1. Latest 20 orders overall from sm_sif_sened
print("Fetching top 20 overall...")
sql1 = """
SELECT TOP 20 
    s.idn, 
    s.sen_no, 
    CONVERT(VARCHAR(10), s.tarix, 23) as tarix, 
    c.name as customer, 
    s.yekun
FROM sm_sif_sened s
LEFT JOIN sm_kontra c ON s.kontra = c.idn
ORDER BY s.idn DESC
"""
results['top_20_overall'] = query(sql1)
for row in results['top_20_overall']:
    row['customer'] = row['customer'] or 'Bilinməyən'

# 2. Latest 10 Underwear orders
print("Fetching top 10 underwear...")
sql2 = """
SELECT TOP 10 
    s.idn, 
    s.sen_no, 
    CONVERT(VARCHAR(10), s.tarix, 23) as tarix, 
    c.name as customer, 
    g.name as product, 
    e.miqdar
FROM sm_sif_sened s
JOIN sm_sif_sened_el e ON e.es_no = s.idn
JOIN sm_goods g ON e.mal = g.idn
LEFT JOIN sm_kontra c ON s.kontra = c.idn
WHERE (g.class = 20 OR (
    (g.name LIKE '%BOXER%' OR g.name LIKE '%MAYKA%' OR g.name LIKE '%KÜLOT%' OR g.name LIKE '%KULOT%' OR g.name LIKE '%BODY%' OR g.name LIKE '%SLİP%' OR g.name LIKE '%SLIP%') 
    AND (g.name LIKE 'HM-%' OR g.name LIKE 'YM-%' OR g.name LIKE 'TM-%')
))
ORDER BY s.idn DESC
"""
results['top_10_underwear'] = query(sql2)
for row in results['top_10_underwear']:
    row['customer'] = row['customer'] or 'Bilinməyən'

# 3. Latest 5 orders for other categories (last 3 months)
print("Fetching recent categories...")
sql_cats = """
SELECT DISTINCT g.class 
FROM sm_sif_sened s
JOIN sm_sif_sened_el e ON e.es_no = s.idn
JOIN sm_goods g ON e.mal = g.idn
WHERE s.tarix >= DATEADD(month, -3, GETDATE()) 
  AND g.class IS NOT NULL 
  AND g.class != 20
"""
cats = query(sql_cats)

results['other_categories'] = {}
for cat_row in cats:
    c_id = cat_row['class']
    sql_cat_orders = f"""
    SELECT TOP 5 
        s.idn, 
        s.sen_no, 
        CONVERT(VARCHAR(10), s.tarix, 23) as tarix, 
        c.name as customer, 
        g.name as product, 
        e.miqdar
    FROM sm_sif_sened s
    JOIN sm_sif_sened_el e ON e.es_no = s.idn
    JOIN sm_goods g ON e.mal = g.idn
    LEFT JOIN sm_kontra c ON s.kontra = c.idn
    WHERE g.class = {c_id} AND s.tarix >= DATEADD(month, -3, GETDATE())
    ORDER BY s.idn DESC
    """
    cat_orders = query(sql_cat_orders)
    if cat_orders:
        for row in cat_orders:
            row['customer'] = row['customer'] or 'Bilinməyən'
        results['other_categories'][f"Class {c_id}"] = cat_orders

print("Saving to file...")
with open('c:/Users/User/.gemini/antigravity/scratch/backend/extracted_orders.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2, default=str)
print("Done.")
