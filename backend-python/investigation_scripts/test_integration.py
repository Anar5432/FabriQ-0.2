import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders

def test():
    print("Testing corab...")
    data = get_orders('corab')
    found_adonis = False
    for comp, cdata in data['companies'].items():
        if 'EKIN' in comp or 'Adonis' in comp or 'Abdullay' in comp:
            print(f"Found {comp} with {len(cdata['orders'])} orders.")
            for o in cdata['orders']:
                if 'EKIN' in comp or 'Adonis' in o['product_name']:
                    found_adonis = True
                    print(f"  - Order: {o['product_name']}, Qty: {o['qty_ordered']}")
                    
    if not found_adonis:
        print("Did not find Adonis/Ekin! Maybe they are in isci sector?")
        print("Testing isci...")
        data2 = get_orders('isci')
        for comp, cdata in data2['companies'].items():
            if 'EKIN' in comp or 'Adonis' in comp or 'Abdullay' in comp:
                print(f"Found {comp} with {len(cdata['orders'])} orders.")
                for o in cdata['orders']:
                    if 'EKIN' in comp or 'Adonis' in o['product_name']:
                        print(f"  - Order: {o['product_name']}, Qty: {o['qty_ordered']}")
                        
if __name__ == '__main__':
    test()
