import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders
orders_dict = get_orders('isci')

cnt = 0
for c in orders_dict['companies']:
    for o in c['orders']:
        if 'TM-L-Z' in o['cesid'] or 'HM-BETEX11' in o['cesid'] or 'DƏSMAL' in o['cesid'] or 'RİVANA' in o['cesid']:
            print('  -', o['cesid'].encode('utf-8').decode('utf-8'))
            cnt += 1
print('TOTAL ITEMS:', cnt)

