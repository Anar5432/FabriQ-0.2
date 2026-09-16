import os
import sys
import django
import json

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders

res = get_orders('underwear')
stages = res.get('stages', [])

if isinstance(stages, dict):
    for k, v in stages.items():
        print(f"Stage {k} ({v['name']}): {v['count']} orders")
elif isinstance(stages, list):
    for s in stages:
        print(f"Stage {s['id']} ({s['name']}): {s['count']} orders")
else:
    print(stages)
