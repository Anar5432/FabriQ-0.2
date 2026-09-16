import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders
orders_dict = get_orders('isci')

with open('dost_orders_dates.txt', 'w', encoding='utf-8') as f:
    for c in orders_dict['companies']:
        if 'DOST' in c['name'].upper():
            f.write(f"## {c['name']}\n")
            for o in c['orders']:
                if 'DƏSMAL' in o['cesid'] or 'UNİFORMA' in o['cesid'] or 'RİVANA' in o['cesid']:
                    f.write(f"* {o['tarix']} | {o['cesid']}\n")
