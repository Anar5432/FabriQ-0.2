import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_dynamic_ym_ids
from dashboard.erp_connector import query

matched = get_dynamic_ym_ids('isci').split(',')
print('Total matched ids:', len(matched))
rows = query("SELECT idn, name, class FROM sm_goods WHERE name LIKE '%09/0018%'")
found = 0
for r in rows:
    if str(r['idn']) in matched:
        found += 1
        print(r['idn'], str(r['name'].encode('ascii', 'ignore')), r['class'])
print('Found in matched:', found)

