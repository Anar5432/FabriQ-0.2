import os
import sys
import django
import json

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders

try:
    orders_resp = get_orders('isci')
    print("Type of orders_resp:", type(orders_resp))
    if isinstance(orders_resp, dict):
        if 'data' in orders_resp:
            orders = orders_resp['data']
        else:
            orders = list(orders_resp.values())
    elif isinstance(orders_resp, tuple):
        orders = orders_resp[0]
    else:
        orders = orders_resp
        
    print(f"Type of orders: {type(orders)}")
    print(f"Total orders fetched: {len(orders)}")
    
    if len(orders) > 0:
        print(f"Type of first element: {type(orders[0])}")
        print(f"First element: {orders[0]}")
    
    if isinstance(orders, list) and len(orders) > 0 and isinstance(orders[0], dict):
        missing_id = [o for o in orders if not o.get('order_id')]
        missing_number = [o for o in orders if not o.get('sen_no') or str(o.get('sen_no')).strip() == '' or str(o.get('sen_no')) == 'None']
        
        print(f"Missing order_id: {len(missing_id)}")
        for o in missing_id[:5]: print(o)
            
        print(f"Missing sen_no (Number): {len(missing_number)}")
        for o in missing_number: print(o['order_id'], o['sen_no'], o['company_name'], o['order_total'])

except Exception as e:
    import traceback
    traceback.print_exc()
