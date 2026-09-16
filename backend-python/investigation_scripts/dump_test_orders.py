import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_orders

data = get_orders('isci')

with open('C:/Users/User/.gemini/antigravity/brain/df34275f-a4c2-4d4e-b2a9-3591daafd7e5/test_orders_review.md', 'w', encoding='utf-8') as f:
    f.write('# Dashboard Test Orders Review\n\n')
    f.write('Below is a diverse list of orders exactly as the backend returns them for the **İşçi geyimi** dashboard. You can use this list to manually cross-check the UI.\n\n')
    
    f.write('## 1. Tamamlandı (Completed) Orders\n')
    f.write('These orders are fully delivered (`qaliq = 0`). They should appear in the UI with a Green `Tamamlandı` badge.\n\n')
    f.write('| Sifariş № | Müştəri | Çeşid | Miqdar | Status |\n')
    f.write('|---|---|---|---|---|\n')
    count = 0
    for c in data['companies']:
        for o in c['orders']:
            if o['status'] == 'Tamamlandı' and count < 10:
                f.write(f"| {o['id']} | {c['name']} | {o['cesid']} | {o['miqdar']} | {o['status']} |\n")
                count += 1
                
    f.write('\n## 2. Davam edir (In Progress) Orders\n')
    f.write('These orders have begun production or material preparation.\n\n')
    f.write('| Sifariş № | Müştəri | Çeşid | Miqdar | Mərhələ | Status |\n')
    f.write('|---|---|---|---|---|---|\n')
    count = 0
    for c in data['companies']:
        for o in c['orders']:
            if o['status'] == 'Davam edir' and count < 10:
                f.write(f"| {o['id']} | {c['name']} | {o['cesid']} | {o['miqdar']} | {o['phase_name']} | {o['status']} |\n")
                count += 1
                
    f.write('\n## 3. Gözləyir (Waiting) Orders\n')
    f.write('These orders are fresh sales without any production transfers yet.\n\n')
    f.write('| Sifariş № | Müştəri | Çeşid | Miqdar | Mərhələ | Status |\n')
    f.write('|---|---|---|---|---|---|\n')
    count = 0
    for c in data['companies']:
        for o in c['orders']:
            if o['status'] == 'Gözləyir' and count < 10:
                f.write(f"| {o['id']} | {c['name']} | {o['cesid']} | {o['miqdar']} | {o['phase_name']} | {o['status']} |\n")
                count += 1
                
    f.write('\n## 4. Recently Discussed Orders\n')
    f.write('Orders that we specifically investigated to ensure they are returned correctly by the database.\n\n')
    f.write('| Sifariş № | Müştəri | Tarix | Çeşid | Miqdar | Status |\n')
    f.write('|---|---|---|---|---|---|\n')
    for c in data['companies']:
        for o in c['orders']:
            if '4074' in o['id'] or '4181' in o['id']:
                f.write(f"| {o['id']} | {c['name']} | {o['tarix']} | {o['cesid']} | {o['miqdar']} | {o['status']} |\n")
