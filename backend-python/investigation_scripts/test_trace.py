import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import get_sector_rules, query

sector = 'isci'
rules = get_sector_rules(sector)
cls_cond = rules['class_condition']
sql = f"""
        SET NOCOUNT ON;
        SELECT
            s.idn AS order_id,
            s.sen_no,
            s.yekun AS order_total,
            CONVERT(VARCHAR(10), s.tarix, 23) AS tarix,
            s.kontra AS company_id,
            c.name AS company_name,
            e.idn AS line_id,
            e.num AS line_num,
            g.idn AS product_id,
            g.name AS product_name,
            e.miqdar AS qty_ordered,
            e.miqdar AS qty_remaining
        FROM sm_sifaris_form s WITH (NOLOCK)
        JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
        LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
        JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
        WHERE {cls_cond}
          AND s.tarix >= DATEADD(DAY, -60, GETDATE())
"""
base_lines = query(sql)
print('Total base_lines:', len(base_lines))

import copy
from collections import defaultdict

product_balances = defaultdict(lambda: defaultdict(float))
hm_name_to_id = {order['product_name']: order['product_id'] for order in base_lines if order['product_name']}

raw_lines = []
for order in base_lines:
    if order['product_name'] and 'RVANA' in order['product_name']:
        print('FOUND IN BASE:', order['product_name'].encode('ascii','ignore').decode())
        
    qaliq = float(order['qty_remaining'] or 0)
    ordered = float(order['qty_ordered'] or 0)
    delivered = ordered - qaliq
    
    if delivered > 0:
        o_deliv = copy.deepcopy(order)
        o_deliv['qty_remaining'] = 0
        o_deliv['current_phase'] = 6
        raw_lines.append(o_deliv)
        
    if qaliq == 0:
        continue
        
    hm_mal = order['product_id']
    bals = product_balances[hm_mal]
    
    dept_priority = [6, 15, 39, 5, 4, 3, 24, 8, 9]
    remaining_to_find = qaliq
    
    for dept_id in dept_priority:
        if remaining_to_find <= 0:
            break
        available = bals[dept_id]
        if available > 0:
            take = min(available, remaining_to_find)
            bals[dept_id] -= take
            remaining_to_find -= take
            
            o_split = copy.deepcopy(order)
            o_split['qty_remaining'] = take
            o_split['current_phase'] = dept_id
            raw_lines.append(o_split)
            
    if remaining_to_find > 0:
        o_split = copy.deepcopy(order)
        o_split['qty_remaining'] = remaining_to_find
        o_split['current_phase'] = 0
        raw_lines.append(o_split)

print('Total raw_lines:', len(raw_lines))

companies = {}
stages = copy.deepcopy(rules['stages'])

for row in raw_lines:
    cid = row['company_id']
    cname = row['company_name'] or 'Bilinməyən'
    if cid not in companies:
        companies[cid] = {'id': cid, 'name': cname, 'orders': []}
        
    companies[cid]['orders'].append({'cesid': row['product_name']})

print('Companies:', len(companies))
for c in companies.values():
    if 'BAKU ELEC' in c['name'].upper():
        print('Found:', c['name'].encode('ascii','ignore').decode())
        for o in c['orders']:
            if o['cesid'] and 'RVANA' in o['cesid']:
                print(' ->', o['cesid'].encode('ascii','ignore').decode())
