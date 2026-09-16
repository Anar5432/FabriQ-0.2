import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(r'c:\Users\User\.gemini\antigravity\scratch\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()

from dashboard.erp_connector import query

# We want to find:
# 1. Total inventory for materials used in Underwear.
# 2. Total material requirements from ACTIVE Underwear orders.
# 3. Total material requirements from ACTIVE Isci and Corab orders.

# Active orders SQL from queries.py
# Using a simplified version to get active quantities

active_orders_sql = '''
SELECT 
    g.class,
    g.idn AS product_id,
    (e.miqdar - ISNULL(e.sat_miq, 0)) AS qty_remaining
FROM sm_sif_sened s WITH (NOLOCK)
JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
WHERE (e.miqdar - ISNULL(e.sat_miq, 0)) > 0
  AND NOT EXISTS (SELECT 1 FROM sm_sifaris_form sf WITH (NOLOCK) WHERE sf.sifaris = s.idn)
  AND g.class IN (18, 20, 21, 29, 30, 22, 24, 27, 31, 32, 34)
'''
active_orders = query(active_orders_sql)

category_map = {
    18: 'Underwear', 20: 'Underwear',
    21: 'Corab', 29: 'Corab', 30: 'Corab',
    22: 'Isci', 24: 'Isci', 27: 'Isci', 31: 'Isci', 32: 'Isci', 34: 'Isci'
}

# 1. Map products to their smeta materials and qtys
smeta_sql = '''
SELECT 
    satis.mal AS product_id,
    xammal.mal AS mat_id,
    xammal.miqdar AS qty_per_unit,
    mat_g.name AS mat_name
FROM sm_smeta_satis satis WITH (NOLOCK)
JOIN sm_smeta_xammal xammal WITH (NOLOCK) ON satis.es_no = xammal.es_no
JOIN sm_goods mat_g WITH (NOLOCK) ON xammal.mal = mat_g.idn
'''
smeta_rows = query(smeta_sql)

# build product -> materials map
product_materials = {}
mat_names = {}
for r in smeta_rows:
    pid = r['product_id']
    mid = r['mat_id']
    mat_names[mid] = r['mat_name']
    if pid not in product_materials:
        product_materials[pid] = []
    product_materials[pid].append({
        'mat_id': mid,
        'qty_per_unit': float(r['qty_per_unit'])
    })

# 2. Calculate required materials by category
required_by_cat = {'Underwear': {}, 'Corab': {}, 'Isci': {}}

for row in active_orders:
    cat = category_map.get(row['class'])
    if not cat: continue
    
    pid = row['product_id']
    qty_rem = float(row['qty_remaining'])
    
    reqs = product_materials.get(pid, [])
    for r in reqs:
        mid = r['mat_id']
        needed = r['qty_per_unit'] * qty_rem
        
        if mid not in required_by_cat[cat]:
            required_by_cat[cat][mid] = 0
        required_by_cat[cat][mid] += needed

# 3. Get total global inventory for these materials
inv_sql = '''
SELECT mal AS mat_id, SUM(miqdar) AS balance
FROM sm_mal_say WITH (NOLOCK)
WHERE anbar IN (2, 6, 7, 11, 17, 18) AND miqdar > 0
GROUP BY mal
'''
inv_rows = query(inv_sql)
inventory = {r['mat_id']: float(r['balance']) for r in inv_rows}

# Identify underwear materials
underwear_mats = set(required_by_cat['Underwear'].keys())

print("=== UNDERWEAR MATERIAL OVERVIEW ===")
print(f"Total Unique Materials Used by Active Underwear Orders: {len(underwear_mats)}")

top_mats = sorted(underwear_mats, key=lambda m: required_by_cat['Underwear'][m], reverse=True)[:10]
print("\nTop 10 Materials Demanded by Underwear:")
for m in top_mats:
    name = mat_names.get(m, 'Unknown')
    req_under = required_by_cat['Underwear'].get(m, 0)
    req_corab = required_by_cat['Corab'].get(m, 0)
    req_isci = required_by_cat['Isci'].get(m, 0)
    total_req = req_under + req_corab + req_isci
    inv = inventory.get(m, 0)
    print(f"- {name} (ID: {m})")
    print(f"  Required (Underwear): {req_under:,.2f}")
    if req_corab > 0: print(f"  Required (Corab):     {req_corab:,.2f}")
    if req_isci > 0:  print(f"  Required (Isci):      {req_isci:,.2f}")
    print(f"  Total Inventory:      {inv:,.2f}")
    if inv < total_req:
        print(f"  [!] SHORTAGE WARNING: Total Req {total_req:,.2f} > Inv {inv:,.2f}")
    print()
