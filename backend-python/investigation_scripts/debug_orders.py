import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from django.core.cache import cache
from dashboard.queries import get_orders

# Clear cache forcefully just in case
cache.clear()

def debug():
    data = get_orders('isci')
    # data is a dict {'companies': [list of dicts], 'stages': ...}
    comps = data.get('companies', [])
    print("Testing isci for EKIN...")
    for cdata in comps:
        comp = cdata['company_name']
        if 'EKIN' in comp:
            print(f"Found {comp} with {len(cdata['orders'])} orders.")
            for o in cdata['orders']:
                print(f"  - Order: {o['product_name']}, Qty: {o['qty_ordered']}, Phase: {o['phase_name']}")
                        
if __name__ == '__main__':
    debug()
