import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.erp_connector import query

sql = "SELECT idn, name, class FROM sm_goods WHERE name LIKE 'HM-BETEX11/0037 UNİFORMA%'"
rows = query(sql)
with open('xurmayi_raw.txt', 'w', encoding='utf-8') as f:
    for r in rows:
        if 'R-38' in r['name']:
            f.write(repr(r['name']) + '\n')
