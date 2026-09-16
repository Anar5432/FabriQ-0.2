import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.erp_connector import query
rows = query("SELECT idn, class, name FROM sm_goods WITH (NOLOCK)")

target_classes = {22, 24, 27, 31, 32, 34}
hm_prefixes = set()
for r in rows:
    cls = r['class']
    name = r['name'] or ''
    if cls in target_classes and name.startswith('HM-'):
        prefix = name.split('/')[0].split(' ')[0]
        hm_prefixes.add(prefix)

matched_ids = []
for r in rows:
    if r['class'] is None:
        name = r['name'] or ''
        if name.startswith('HM-'):
            hm_equiv = name.split('/')[0].split(' ')[0]
            if hm_equiv in hm_prefixes:
                matched_ids.append(r['idn'])

print('Total hm_prefixes:', len(hm_prefixes))
print('HM-BETEX' in hm_prefixes)
print('Number of matched None-class HM products:', len(matched_ids))

specific_rows = query("SELECT idn FROM sm_goods WHERE name LIKE 'HM-BETEX/09/0018%'")
if specific_rows:
    print('Specific product matched:', specific_rows[0]['idn'] in matched_ids)
