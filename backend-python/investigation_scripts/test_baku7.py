import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders
orders_dict = get_orders('isci')

for c in orders_dict['companies']:
    for o in c['orders']:
        if 'TM-' in o['cesid']:
            print('Customer:', c['name'].encode('ascii', 'ignore').decode(), 'Product:', o['cesid'].encode('ascii', 'ignore').decode())
        if 'HM-BETEX11' in o['cesid']:
            print('Customer:', c['name'].encode('ascii', 'ignore').decode(), 'Product:', o['cesid'].encode('ascii', 'ignore').decode())

