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
    if comp['id'] in (840, 905, None) or comp['name'] == 'Bilinməyən':
        print(f"Company ID: {comp['id']} -> {comp['name']}")
        for order in comp['orders']:
            print(order)
