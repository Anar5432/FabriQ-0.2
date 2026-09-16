import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders

def test():
    print("Testing get_orders for isci...")
    # Get all orders
    result = get_orders('isci')
    print("Keys in result:", result.keys())
    
    # See if MONEX is in pending_lines
    pending = result['pending_lines']
    monex_orders = [o for o in pending if 'MONEX' in str(o.get('company_name', '')).upper()]
    print(f"Found {len(monex_orders)} pending line objects for MONEX")
    
    # Grouped pending orders
    grouped_pending = result['pending']
    print(f"Total customers in grouped pending: {len(grouped_pending)}")
    monex_customer = next((c for c in grouped_pending if 'MONEX' in str(c['company_name']).upper()), None)
    if monex_customer:
        print("MONEX is in grouped pending!")
        print("MONEX orders count:", len(monex_customer['orders']))
        # Show first few dates
        dates = set([o['tarix'] for o in monex_customer['orders']])
        print("Dates for MONEX:", dates)
    else:
        print("MONEX not in grouped pending!")

if __name__ == '__main__':
    test()
