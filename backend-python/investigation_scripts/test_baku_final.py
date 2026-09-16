import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from django.core.cache import cache
cache.clear()
from dashboard.queries import get_orders

orders_dict = get_orders('isci')
cnt = 0
for c in orders_dict['companies']:
    if 'BAKU ELEC' in c['name'].upper():
        print('Found customer:', c['name'].encode('ascii','ignore').decode())
        for o in c['orders']:
            if 'RVANA' in o['cesid'] or 'TM-L-Z' in o['cesid'] or 'HM-BETEX11' in o['cesid']:
                print('  - ', o['cesid'].encode('ascii','ignore').decode())
                cnt += 1
print('TOTAL ITEMS:', cnt)
