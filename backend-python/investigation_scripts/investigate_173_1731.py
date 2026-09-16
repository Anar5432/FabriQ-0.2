import os
import sys
import django
import json

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

def default(o):
    return str(o)

sql = "SELECT idn, name, fol_idn, folder FROM sm_kontra WHERE idn IN (173, 1731)"
try:
    print(json.dumps(query(sql), default=default, indent=2))
except Exception as e:
    print(e)
