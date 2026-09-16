import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders

data = get_orders('isci')
x_c = 0
ya_c = 0
lz_c = 0
for c in data['companies']:
    for o in c['orders']:
        name = o['cesid'].upper()
        if 'XURMAYI' in name:
            print('XURMAYI:', c['name'].encode('ascii', 'ignore').decode(), name.encode('ascii', 'ignore').decode())
            x_c += 1
        if 'AYAQ D' in name:
            print('AYAQ D:', c['name'].encode('ascii', 'ignore').decode(), name.encode('ascii', 'ignore').decode())
            ya_c += 1
        if '50X90' in name or 'XOVLU' in name:
            print('50X90:', c['name'].encode('ascii', 'ignore').decode(), name.encode('ascii', 'ignore').decode())
            lz_c += 1
print('X:', x_c, 'YA:', ya_c, 'LZ:', lz_c)

