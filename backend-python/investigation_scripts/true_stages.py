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
    
    count = 0
    for comp in data['companies']:
        for order in comp['orders']:
            # We want to see orders from sm_sifaris_form or sm_sif_sened which are showing as Tamamlandi incorrectly.
            # Usually they are recent. Let's just pick recent ones.
            if order['tarix'] >= '2026-06-01' and order.get('order_id'):
                out.write(f"- Company: {comp['name']}, Order: {order['cesid']}, Date: {order['tarix']}, "
                          f"Ordered: {order['miqdar']}, True Phase: {order['phase_name']} (Phase ID: {order['current_phase']})\n")
                count += 1
                if count >= 15:
                    break
        if count >= 15:
            break

    with io.open("true_stages.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
