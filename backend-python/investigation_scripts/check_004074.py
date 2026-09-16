import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders

data = get_orders('isci')
print('ORDERS IN DASHBOARD FOR 004074:')
count = 0
for c in data['companies']:
    for o in c['orders']:
        if '4074' in str(o['id']):
            count += 1
            print(c['name'].encode('ascii','ignore').decode(), o['id'], str(o['miqdar']).encode('ascii','ignore').decode(), o['cesid'].encode('ascii','ignore').decode())
print('TOTAL = ', count)

