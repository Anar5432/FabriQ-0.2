import os
import sys
import django
import json

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders, query

res = get_orders('underwear')
companies = res.get('companies', [])

sample_pids = []

for c in companies:
    for o in c.get('orders', []):
        if o.get('current_phase') == '0' or o.get('match_type') == 'order_id':
            # wait, how is stage_key passed? it's not in the order object, it's just counted!
            # wait, in get_orders, where is stage_key stored on the order object?
            pass

# actually get_orders doesn't store stage_key in the order dict, it only uses it to group into companies/stages.
# let's just get the first 10 orders from get_orders and see their product_ids
c = 0
for comp in companies:
    for o in comp.get('orders', []):
        sample_pids.append(str(o['product_id']))
        c += 1
        if c > 10: break
    if c > 10: break

pid_str = ",".join(sample_pids)
print(f"Sample PIDs: {pid_str}")

sql = f"""
SELECT s.mal, sm.tesdiq 
FROM sm_smeta_satis s 
JOIN sm_smeta sm ON s.es_no = sm.idn
WHERE s.mal IN ({pid_str})
"""
smeta_check = query(sql)
print(f"SMETA Check: {smeta_check}")
