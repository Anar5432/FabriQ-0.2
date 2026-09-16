import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = "SELECT idn, name, emp, qeyd, unvan FROM sm_kontra WHERE idn = 7896"
try:
    print("sm_kontra 7896:", query(sql))
except Exception as e:
    pass

