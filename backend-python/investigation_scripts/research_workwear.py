# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath('C:/Users/User/.gemini/antigravity/scratch/backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()
from dashboard.erp_connector import query

sys.stdout.reconfigure(encoding='utf-8')

# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath('C:/Users/User/.gemini/antigravity/scratch/backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()
from dashboard.erp_connector import query

print("--- Check YM and HM linkage ---")
sql = """
SELECT TOP 10 
    s.idn as sales_order_id,
    g_hm.name as ordered_item,
    g_ym.name as produced_item,
    t.sobe2 as curr_stage
FROM sm_kontr_sat s
JOIN sm_kontr_sat_el e ON e.es_no = s.idn
JOIN sm_goods g_hm ON e.mal = g_hm.idn
JOIN sm_goods g_ym ON SUBSTRING(g_ym.name, 4, LEN(g_ym.name)) = SUBSTRING(g_hm.name, 4, LEN(g_hm.name)) 
    AND g_ym.name LIKE 'YM-%' AND g_hm.name LIKE 'HM-%'
JOIN sm_sob_trans_el tel ON tel.mal = g_ym.idn
JOIN sm_sob_trans t ON t.idn = tel.es_no AND t.tesdiq = 1
WHERE g_hm.class = 27 AND e.qaliq > 0
ORDER BY s.tarix DESC, t.tarix DESC
"""
print(query(sql))










