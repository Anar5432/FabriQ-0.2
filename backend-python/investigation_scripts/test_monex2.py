import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders

def test():
    print("Testing get_orders for isci...")
    # Get all orders
    result = get_orders('isci')
    companies = result['companies']
    
    monex_customer = next((c for c in companies if 'MONEX' in str(c['name']).upper()), None)
    if monex_customer:
        print("MONEX is in grouped pending!")
        print("MONEX orders count:", len(monex_customer['orders']))
        # Show all dates
        for o in monex_customer['orders']:
            print(f"ID: {o['id']}  Cesid: {o['cesid']}  Tarix: {o['tarix']} ({o['raw_tarix']})  Miqdar: {o['miqdar']} Status: {o['status']}")
    else:
        print("MONEX not in grouped pending!")

if __name__ == '__main__':
    test()
