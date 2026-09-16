import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.erp_connector import query

sql = "SELECT idn, name, class FROM sm_goods WHERE UPPER(name) LIKE '%XURMA%'"
rows = query(sql)
for r in rows:
    print(r['name'].encode('ascii', 'replace').decode())
