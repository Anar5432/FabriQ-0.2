import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = "SELECT idn, name FROM sm_kontra WHERE idn = 474"
print("474:", query(sql))

sql2 = "SELECT TOP 1 * FROM sm_kontra WHERE name LIKE '%Ilqar%'"
print("Any Ilqar in kontra?:", query(sql2))
