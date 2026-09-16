import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

res = query("SELECT p.name as pos, e.name as emp_name FROM sm_emp e LEFT JOIN sm_position p ON e.position = p.idn WHERE e.ise_son IS NULL ORDER BY p.name, e.name")

data = {}
for r in res:
    p = r['pos'] or 'Bilinmir'
    n = r['emp_name']
    if p not in data: data[p] = []
    data[p].append(n)

with open('worker_list.txt', 'w', encoding='utf-8') as f:
    for p, names in data.items():
        f.write(f'# {p} ({len(names)})\n')
        for n in names:
            f.write(f'- {n}\n')
