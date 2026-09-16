# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders

def test():
    out = io.StringIO()
    try:
        data = get_orders('isci')
        for comp in data['companies']:
            if 'AZƏRSU' in comp['name'] or 'AZERSU' in comp['name']:
                out.write(f"\n--- {comp['name']} ---\n")
                out.write(f"Total Orders: {len(comp['orders'])}\n")
                
                # Check if YM-BETEX/01/0119 is there
                found = False
                for order in comp['orders']:
                    if '01/0119' in order['cesid']:
                        found = True
                        out.write(f"Found: {order['cesid']} | Ordered: {order.get('qty_ordered')} | Remaining: {order.get('qty_remaining')} | Line: {order.get('order_number')}\n")
                if not found:
                    out.write("NO 01/0119 PRODUCTS FOUND FOR AZƏRSU!\n")
    except Exception as e:
        import traceback
        traceback.print_exc()

    with io.open("test_azersu.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    test()
