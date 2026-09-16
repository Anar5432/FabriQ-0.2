import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = "SELECT TOP 10 * FROM sm_kmd WHERE mezmun LIKE '%lqar bin%'"
print("sm_kmd:")
try:
    for r in query(sql):
        print(r)
except Exception as e:
    print(e)
    
sql2 = "SELECT TOP 10 * FROM emel_lar WHERE mezmun LIKE '%lqar bin%'"
print("\nemel_lar:")
try:
    for r in query(sql2):
        print(r)
except Exception as e:
    print(e)
