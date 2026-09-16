import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders

orders = get_orders('underwear')

found_weird = []
for cdata in orders:
    for o in cdata.get('orders', []):
        try:
            oid = int(o['order_id'])
            if oid > 10000:
                found_weird.append((oid, cdata['name']))
        except:
            pass

print(f"Total weird orders remaining: {len(found_weird)}")
for w in found_weird:
    print(w)
