import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = "SELECT TOP 10 * FROM hes_plan WHERE name LIKE '%lqar%'"
try:
    print("hes_plan:", query(sql))
except Exception as e:
    print(e)
