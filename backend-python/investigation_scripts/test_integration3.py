import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders

def test():
    data = get_orders('corab')
    # print the keys if it's a dict
    if isinstance(data, dict):
        print("Keys:", data.keys())
        companies = data.get('companies', {})
        for comp, cdata in companies.items():
            if 'EKIN' in comp or 'Adonis' in comp or 'Abdullay' in comp:
                print(f"Found {comp} with {len(cdata['orders'])} orders.")
                for o in cdata['orders']:
                    if 'EKIN' in comp or 'Adonis' in o['product_name']:
                        print(f"  - Order: {o['product_name']}, Qty: {o['qty_ordered']}")
                        
    else:
        print("Data is a list! Length:", len(data))

if __name__ == '__main__':
    test()
