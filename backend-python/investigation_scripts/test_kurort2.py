import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders

orders_dict = get_orders('isci')

found = []
for c in orders_dict['companies']:
    if 'KURORT' in c['name']:
        for o in c['orders']:
            print(o['cesid'].encode('ascii','ignore').decode(), o['miqdar'], o['status'])

