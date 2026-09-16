import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders

from django.core.cache import cache
cache.clear()

data = get_orders('isci')

with open('debug_get_orders.txt', 'w', encoding='utf-8') as f:
    f.write(f"Total companies: {len(data['companies'])}\n")
    for c in data['companies']:
        for o in c['orders']:
            if 'XURMAYI' in o['cesid']:
                f.write(f"XURMAYI: {c['name']} -> {o['cesid']}\n")
            if 'AYAQ' in o['cesid']:
                f.write(f"AYAQ: {c['name']} -> {o['cesid']}\n")
            if '50x90' in o['cesid'] or '50X90' in o['cesid'] or 'XOVLU' in o['cesid']:
                f.write(f"L-Z: {c['name']} -> {o['cesid']}\n")
