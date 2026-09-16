import os
import sys
import django
import json
import time

sys.path.append(r'c:\Users\User\.gemini\antigravity\scratch\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders

start = time.time()
orders_data = get_orders('isci')
end = time.time()

total_mats = 0
total_mats_json_len = 0
order_count = 0

for c in orders_data['companies']:
    for o in c['orders']:
        order_count += 1
        mats = o.get('materials', [])
        total_mats += len(mats)
        mats_json = o.get('materials_json', '')
        total_mats_json_len += len(mats_json)
        
print(f"Time: {end - start:.2f}s")
print(f"Order Count: {order_count}")
print(f"Total Mats: {total_mats}")
print(f"Total Mats JSON Len: {total_mats_json_len} chars")

