import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = "SELECT * FROM sm_sifaris WHERE idn = 1104"
try:
    print("sm_sifaris 1104:")
    for r in query(sql):
        print(r)
except Exception as e:
    print(e)
