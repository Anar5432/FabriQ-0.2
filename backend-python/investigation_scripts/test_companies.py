# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders

def check_logic():
    out = io.StringIO()
    data = get_orders('isci')
    
    # search for MONEX, ADONIS/ADONES, EKIN
    for comp in data['companies']:
        name = comp['name'].upper()
        if 'MONEX' in name or 'ADONES' in name or 'EKIN' in name or 'ADONIS' in name or 'ƏKİN' in name:
            out.write(f"\n--- Company: {name} ---\n")
            for order in comp['orders']:
                out.write(f" - {order['cesid']} | Miqdar: {order['miqdar']} | Date: {order['tarix']} | Stage: {order['phase_name']}\n")

    with io.open("comp_test.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
