import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders

data = get_orders('isci')

found_jan = False
found_feb = False
found_mar = False

with open('C:/Users/User/.gemini/antigravity/brain/df34275f-a4c2-4d4e-b2a9-3591daafd7e5/historical_orders.md', 'w', encoding='utf-8') as f:
    f.write('# Historical Test Orders (3, 4, and 5 Months Ago)\n\n')
    f.write('| Ay (Month) | Sifariş № | Müştəri | Tarix | Çeşid | Status |\n')
    f.write('|---|---|---|---|---|---|\n')
    for c in data['companies']:
        for o in c['orders']:
            tarix = str(o['raw_tarix'])
            if '2026-01-' in tarix and not found_jan:
                f.write(f"| 5 Months Ago (Jan) | {o['id']} | {c['name']} | {o['tarix']} | {o['cesid']} | {o['status']} |\n")
                found_jan = True
            if '2026-02-' in tarix and not found_feb:
                f.write(f"| 4 Months Ago (Feb) | {o['id']} | {c['name']} | {o['tarix']} | {o['cesid']} | {o['status']} |\n")
                found_feb = True
            if '2026-03-' in tarix and not found_mar:
                f.write(f"| 3 Months Ago (Mar) | {o['id']} | {c['name']} | {o['tarix']} | {o['cesid']} | {o['status']} |\n")
                found_mar = True
            
            if found_jan and found_feb and found_mar:
                break
        if found_jan and found_feb and found_mar:
            break
