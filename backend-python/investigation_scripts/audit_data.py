import sys, os, json
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(r'c:\Users\User\.gemini\antigravity\scratch\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()

from dashboard.erp_connector import query

print("--- AUDITING DATA ACCURACY ---")

# 1. Fetch ALL Active Orders from ALL categories (Socks, Corporate, Underwear)
active_orders_sql = '''
SELECT 
    s.idn AS order_id,
    e.idn AS line_id,
    g.class,
    g.idn AS product_id,
    g.name AS product_name,
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

print(f"Total active order lines across ALL categories: {len(active_orders)}")

# 2. Audit SMETA logic (Material Requirements)
# Does every active product actually have a SMETA definition?
smeta_sql = '''
SELECT DISTINCT satis.mal AS product_id
FROM sm_smeta_satis satis WITH (NOLOCK)
JOIN sm_smeta_xammal xammal WITH (NOLOCK) ON satis.es_no = xammal.es_no
'''
smeta_products = {r['product_id'] for r in query(smeta_sql)}

missing_smeta_count = 0
missing_smeta_by_cat = defaultdict(int)

for row in active_orders:
    pid = row['product_id']
    cat = category_map.get(row['class'])
    if pid not in smeta_products:
        missing_smeta_count += 1
        missing_smeta_by_cat[cat] += 1

print("\n--- SMETA (MATERIAL REQUIREMENTS) ACCURACY ---")
if missing_smeta_count > 0:
    print(f"WARNING: {missing_smeta_count} out of {len(active_orders)} active order lines DO NOT have a SMETA defined in the database!")
    print("Breakdown of missing SMETA by category:")
    for cat, count in missing_smeta_by_cat.items():
        print(f"  - {cat}: {count} orders missing SMETA")
else:
    print("SUCCESS: 100% of active order lines have a SMETA defined.")

# 3. Audit Inventory logic
# Are there weird things in sm_mal_say?
inv_sql = '''
SELECT mal AS mat_id, SUM(miqdar) AS balance
FROM sm_mal_say WITH (NOLOCK)
WHERE anbar IN (2, 6, 7, 11, 17, 18)
GROUP BY mal
'''
inv_rows = query(inv_sql)

negative_balances = 0
zero_balances = 0
positive_balances = 0

for r in inv_rows:
    bal = float(r['balance'])
    if bal < 0:
        negative_balances += 1
    elif bal == 0:
        zero_balances += 1
    else:
        positive_balances += 1

print("\n--- INVENTORY DATA (sm_mal_say) OVERVIEW ---")
print(f"Total unique materials in tracked warehouses (2, 6, 7, 11, 17, 18): {len(inv_rows)}")
print(f"  - Positive Balance: {positive_balances}")
print(f"  - Zero Balance: {zero_balances}")
print(f"  - Negative Balance: {negative_balances}")

if negative_balances > 0:
    print("WARNING: Negative balances exist! This suggests potential data entry issues or out-of-order transactions in the ERP.")
