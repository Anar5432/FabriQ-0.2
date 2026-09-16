import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders

def test():
    data = get_orders('corab')
    companies = data.get('companies', [])
    for cdata in companies:
        comp = cdata['company_name']
        if 'EKIN' in comp or 'Adonis' in comp or 'Abdullay' in comp:
            print(f"Found {comp} with {len(cdata['orders'])} orders.")
            for o in cdata['orders']:
                if 'EKIN' in comp or 'Adonis' in o['product_name'] or 'Adonis' in str(o.get('product_name')):
                    print(f"  - Order: {o['product_name']}, Qty: {o['qty_ordered']}")
                        
if __name__ == '__main__':
    test()
