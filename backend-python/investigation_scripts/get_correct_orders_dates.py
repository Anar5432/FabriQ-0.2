import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders
orders_dict = get_orders('isci')

with open('correct_orders_with_dates.txt', 'w', encoding='utf-8') as f:
    for c in orders_dict['companies']:
        if 'BAKU' in c['name'].upper() or 'DOST' in c['name'].upper() or 'TENG' in c['name'].upper():
            f.write(f"## {c['name']}\n")
            for o in c['orders']:
                if 'YM-BETEX' in o['cesid'] or 'TM-SOSAL' in o['cesid'] or 'HM-BETEX' in o['cesid']:
                    # format output with date
                    f.write(f"* {o['tarix']} | {o['cesid']}\n")
            f.write('\n')
