import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders

orders = get_orders('isci')
print('Number of companies:', len(orders['companies']))
found = False
for c in orders['companies']:
    for o in c['orders']:
        if o.get('sen_no') == '004181':
            found = True
            print('Found 004181 in get_orders!')
if not found:
    print('004181 not found. Companies with 4181? None')

