import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.erp_connector import query

sql = "SELECT idn, name, class FROM sm_goods WHERE name LIKE 'HM-BETEX11/0037 UNİFORMA%'"
rows = query(sql)
for r in rows:
    print(r['name'].encode('ascii', 'ignore').decode())

sql2 = "SELECT idn, name, class FROM sm_goods WHERE name LIKE '%XURMAYI%'"
rows2 = query(sql2)
for r in rows2:
    print('FOUND XURMAYI:', r['name'].encode('ascii', 'ignore').decode())

