import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import get_orders

result = get_orders('underwear')
companies = result['companies'] if isinstance(result, dict) else result

for comp in companies:
    if comp['name'] == 'Bilinməyən':
        print(f"Bilinməyən Group: cid={comp['id']}, type={type(comp['id'])}")
        for order in comp['orders']:
            print(f"  Order ID: {order['order_id']}, order_total: {order.get('order_total')}")
