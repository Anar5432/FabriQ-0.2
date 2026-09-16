import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders
orders_dict = get_orders('isci')

xurmayi_found = 0
yasil_found = 0
ayaq_found = 0
lz_found = 0

for c in orders_dict['companies']:
    for o in c['orders']:
        name = o['cesid'].upper()
        if 'XURMAYI' in name:
            print('FOUND XURMAYI:', c['name'].encode('ascii', 'ignore').decode(), name.encode('ascii', 'ignore').decode())
            xurmayi_found += 1
        if 'YAIL' in name or 'YAŞIL' in o['cesid'].upper():
            print('FOUND YASIL:', c['name'].encode('ascii', 'ignore').decode(), name.encode('ascii', 'ignore').decode())
            yasil_found += 1
        if 'AYAQ D' in name:
            print('FOUND AYAQ:', c['name'].encode('ascii', 'ignore').decode(), name.encode('ascii', 'ignore').decode())
            ayaq_found += 1
        if '50X90' in name or 'XOVLU' in name:
            print('FOUND 50x90/XOVLU:', c['name'].encode('ascii', 'ignore').decode(), name.encode('ascii', 'ignore').decode())
            lz_found += 1

print('Totals:')
print('Xurmayi:', xurmayi_found)
print('Yasil:', yasil_found)
print('Ayaq:', ayaq_found)
print('L-Z 50x90:', lz_found)

