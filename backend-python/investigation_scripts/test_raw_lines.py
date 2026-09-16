import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders

orders_dict = get_orders('isci')

found = []
for c in orders_dict['companies']:
    for o in c['orders']:
        if o.get('id') and '4181' in str(o.get('id')):
            found.append((c['name'], o))

print(f'Found {len(found)} instances of 4181 in orders_dict')
for cname, o in found:
    print(cname.encode('ascii','ignore').decode(), o['cesid'].encode('ascii','ignore').decode(), o['id'], o['status'], o['stage_id'])

