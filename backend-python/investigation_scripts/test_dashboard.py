# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath('C:/Users/User/.gemini/antigravity/scratch/backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()
from dashboard.queries import get_orders

data = get_orders('isci')
stages = data['stages']

print("--- Isci Geyimi Dashboard Stages ---")
for s in stages:
    print(f"{s['id']}: {s['count']} orders (capacity: {s['cap']}, pct: {s['pct']}%)")


