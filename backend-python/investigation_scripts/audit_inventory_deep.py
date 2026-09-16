import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(r'c:\Users\User\.gemini\antigravity\scratch\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()

from dashboard.erp_connector import query

print("--- INVENTORY DEEP DIVE RESEARCH ---")

# 1. Get the list of all warehouses to understand what they are
print("\n1. WAREHOUSE MASTER LIST (sm_depo):")
anbar_sql = "SELECT idn, name FROM sm_depo WITH (NOLOCK) ORDER BY idn"
try:
    warehouses = query(anbar_sql)
    for w in warehouses:
        print(f"  - Warehouse {w['idn']}: {w['name']}")
except Exception as e:
    print(f"Error fetching warehouses: {e}")

# 2. Check sm_mal_say distribution across ALL warehouses
print("\n2. sm_mal_say DISTRIBUTION (Total Stock per Warehouse):")
mal_say_sql = '''
SELECT a.idn, a.name, SUM(ms.miqdar) as total_qty, COUNT(DISTINCT ms.mal) as unique_items
FROM sm_mal_say ms WITH (NOLOCK)
LEFT JOIN sm_depo a WITH (NOLOCK) ON ms.anbar = a.idn
GROUP BY a.idn, a.name
ORDER BY a.idn
'''
try:
    dist = query(mal_say_sql)
    for d in dist:
        print(f"  - Warehouse {d['idn']} ({d['name']}): {d['total_qty']:,.2f} total items, {d['unique_items']} unique products")
except Exception as e:
    print(f"Error fetching sm_mal_say: {e}")

# 3. Look for other inventory-related tables in the schema
print("\n3. SEARCHING FOR OTHER INVENTORY/STOCK TABLES:")
schema_sql = '''
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE' 
  AND (TABLE_NAME LIKE '%anbar%' OR TABLE_NAME LIKE '%say%' OR TABLE_NAME LIKE '%stok%' OR TABLE_NAME LIKE '%qaliq%' OR TABLE_NAME LIKE '%xammal%')
ORDER BY TABLE_NAME
'''
try:
    tables = query(schema_sql)
    for t in tables:
        print(f"  - {t['TABLE_NAME']}")
except Exception as e:
    print(f"Error fetching schema: {e}")

