# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath('C:/Users/User/.gemini/antigravity/scratch/backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()
from dashboard.erp_connector import query

import sys
sys.stdout.reconfigure(encoding='utf-8')

# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath('C:/Users/User/.gemini/antigravity/scratch/backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()
from dashboard.erp_connector import query
sys.stdout.reconfigure(encoding='utf-8')

print('\n--- Production Phases (Faza) for İşçi Geyimi ---')
sql = f'''
SELECT TOP 10 f.idn, f.name, COUNT(*) as count 
FROM sm_good_ist_el e
JOIN sm_goods g ON e.mal = g.idn
JOIN sm_faza f ON e.son_faza = f.idn
WHERE g.class = 27
GROUP BY f.idn, f.name
ORDER BY count DESC
'''
print(query(sql))

print('\n--- Recent Orders (last 12 months) ---')
sql2 = f'''
SELECT COUNT(*) as total_orders, SUM(e.miqdar) as total_qty, SUM(e.qaliq) as total_backlog
FROM sm_kontr_sat s
JOIN sm_kontr_sat_el e ON s.idn = e.es_no
JOIN sm_goods g ON e.mal = g.idn
WHERE g.class = 27
'''
print(query(sql2))

