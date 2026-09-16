import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import query

sector = 'isci'
target_classes = {
    42981, 42982, 42983, 42984, 42985, 42986, 42987, 43224, 43225, 43226, 43227, 43228,
    43229, 43230, 44181, 44182, 44183, 44184, 44185, 44186, 45293, 45450, 45452, 45453,
    45455, 45669, 45672, 45674, 45864, 46006, 46011, 46473, 46580, 46581, 46585, 46830,
    46831, 46841, 47101, 47102, 47103, 47265, 47266, 47346, 47348, 47350, 47447, 47451,
    47551, 47552, 48243, 48332, 48430, 48431, 48432, 48873, 49830, 50130, 50355, 50571,
    50650, 50849, 50920, 50965, 50966, 51097
}

sql = "SELECT idn, name, class FROM sm_goods"
rows = query(sql)
hm_prefixes = set()

for r in rows:
    cls = r['class']
    name = r['name'] or ''
    if cls in target_classes and name.startswith('HM-'):
        prefix = name.split('/')[0].split(' ')[0]
        hm_prefixes.add(prefix)

print("HM Prefixes:", hm_prefixes)

matched = []
for r in rows:
    if r['class'] is None:
        name = r['name'] or ''
        if name.startswith('TM-'):
            base_name = name.split('/')[0].split(' ')[0]
            hm_equiv = base_name.replace('TM-', 'HM-', 1)
            if hm_equiv in hm_prefixes:
                matched.append(name)
            elif 'DSMALI' in name:
                print(f"FAILED TO MATCH: {name} | base_name: {base_name} | hm_equiv: {hm_equiv}")

print("Matched TM- items:", matched)
