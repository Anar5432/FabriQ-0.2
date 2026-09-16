import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = "SELECT TOP 5 * FROM sm_vetendas WHERE name LIKE '%lqar%'"
try:
    print("sm_vetendas Ilqar:", query(sql))
except Exception as e:
    print("Error:", e)
    
sql2 = "SELECT TOP 1 * FROM sm_vetendas WHERE idn = 1731 OR idn = 7896"
try:
    print("sm_vetendas 1731/7896:", query(sql2))
except Exception as e:
    pass

