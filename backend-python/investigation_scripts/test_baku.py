import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders

orders_dict = get_orders('isci')

for c in orders_dict['companies']:
    if 'BAKU ELEC' in c['name'].upper():
        for o in c['orders']:
            if 'RVANA' in o['cesid']:
                print('FOUND:', o['cesid'].encode('ascii','ignore').decode())

