# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders

def check_logic():
    out = io.StringIO()
    data = get_orders('corab')
    
    count = 0
    for comp in data['companies']:
        for order in comp['orders']:
            if order.get('order_id') and order.get('current_phase') != 0:
                out.write(f"- Company: {comp['name']}, Order: {order['cesid']}, Date: {order['tarix']}, "
                          f"Ordered: {order['miqdar']}, Final Phase: {order['current_phase']}\n")
                count += 1
                if count >= 10:
                    break
        if count >= 10:
            break

    with io.open("corab_phases.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
