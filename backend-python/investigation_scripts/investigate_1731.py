import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = "SELECT TOP 10 * FROM sm_kmd WHERE kontra = '1731' OR kon_name LIKE '%1731%'"
try:
    print("sm_kmd for 1731:")
    for r in query(sql):
        print(r)
except Exception as e:
    pass

sql2 = "SELECT TOP 10 * FROM emel_lar WHERE desc4 = '1731'"
try:
    print("\nemel_lar for 1731:")
    for r in query(sql2):
        print(r)
except Exception as e:
    pass

sql3 = "SELECT TOP 10 * FROM sm_sif_sened WHERE kontra = 1731"
try:
    print("\nsm_sif_sened for 1731:")
    for r in query(sql3):
        print(r['sen_no'], r['serh'])
except Exception as e:
    pass
