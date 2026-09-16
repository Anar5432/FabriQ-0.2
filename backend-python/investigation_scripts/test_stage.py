import os
import io
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders
data = get_orders('isci')

with io.open('counts.txt', 'w', encoding='utf-8') as f:
    f.write(str([(s['name'], s['count']) for s in data['stages']]))
