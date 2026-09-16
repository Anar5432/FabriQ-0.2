import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders

data = get_orders('isci')
found = False
for c in data['companies']:
    for o in c['orders']:
        if '4181' in o['id']:
            print('FOUND ORDER', c['name'].encode('ascii','ignore').decode(), o['cesid'].encode('ascii','ignore').decode(), o['status'], o['id'], o['raw_tarix'])
            found = True
if not found:
    print('Order 4181 not found in get_orders output')

