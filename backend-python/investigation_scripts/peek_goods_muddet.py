import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django; django.setup()
from dashboard.erp_connector import query

sql = "SELECT TOP 10 name, muddet FROM sm_goods WHERE class = 27 AND muddet IS NOT NULL AND muddet > 0 ORDER BY muddet DESC"
rows = query(sql)
print("Products with 'muddet' (duration) > 0:")
for r in rows:
    print(r)

if not rows:
    print("No products have a muddet > 0.")
    
# Let's also check if there is an operations routing table, sometimes named sm_tech_karta or similar
sql2 = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE '%tech%' OR TABLE_NAME LIKE '%tex%'"
print("\nTables related to Tech/Tex:")
for r in query(sql2):
    print(r['TABLE_NAME'])

