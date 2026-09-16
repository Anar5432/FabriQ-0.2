import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(r'c:\Users\User\.gemini\antigravity\scratch\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()

from dashboard.erp_connector import query

# Let's check inventory for BOXER REZİN EMZO (LASTİK) (ID: 2863) across ALL warehouses
inv_sql = '''
SELECT anbar, SUM(miqdar) AS balance
FROM sm_mal_say WITH (NOLOCK)
WHERE mal = 2863
GROUP BY anbar
'''
rows = query(inv_sql)
print("Warehouse balances for BOXER REZİN EMZO (LASTİK) (ID: 2863):")
if not rows:
    print("NO RECORDS FOUND IN ANY WAREHOUSE.")
for r in rows:
    print(f"Warehouse {r['anbar']}: {r['balance']}")

# Check another one: SÜPRƏM LİKRALI NE 30/1 QARA 170 QR EN 185 SM (ID: 6143)
inv_sql2 = '''
SELECT anbar, SUM(miqdar) AS balance
FROM sm_mal_say WITH (NOLOCK)
WHERE mal = 6143
GROUP BY anbar
'''
rows2 = query(inv_sql2)
print("\nWarehouse balances for SÜPRƏM LİKRALI NE 30/1 QARA (ID: 6143):")
if not rows2:
    print("NO RECORDS FOUND IN ANY WAREHOUSE.")
for r in rows2:
    print(f"Warehouse {r['anbar']}: {r['balance']}")
