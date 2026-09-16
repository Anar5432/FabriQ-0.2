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
        if o['id'] == '4181' or o['id'] == '004181':
            print('FOUND ORDER', c['name'].encode('ascii','ignore').decode(), o['cesid'].encode('ascii','ignore').decode(), o['status'])
            found = True
if not found:
    print('Order 4181 not found in get_orders output')

