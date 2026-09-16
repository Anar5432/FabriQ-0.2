import sys, os
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django; django.setup()
from dashboard.queries import get_orders

print("=== Testing CORAB from DB ===")
data = get_orders('corab')
companies = data['companies']
print(f"Corab companies: {len(companies)}")
for c in companies[:5]:
    print(f"  - {c['name']} ({len(c['orders'])} orders)")

print()
print("=== Testing ISCI from DB ===")
data2 = get_orders('isci')
companies2 = data2['companies']
print(f"Isci companies: {len(companies2)}")
for c in companies2[:5]:
    print(f"  - {c['name']} ({len(c['orders'])} orders)")
