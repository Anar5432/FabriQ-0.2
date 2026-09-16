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
        if '4181' in str(o['id']):
            print('FOUND ORDER:', o['id'], o['cesid'].encode('ascii','ignore').decode(), o['status'].encode('ascii','ignore').decode(), o['miqdar'])
            found = True
if not found:
    print('Order 4181 not found in get_orders output')

