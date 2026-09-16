import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django; django.setup()
from dashboard.erp_connector import query

print("--- DEEP DATA ANALYSIS ---")
sql = """
SELECT TOP 5
    hm.name AS product,
    hm.muddet AS db_muddet,
    MIN(t.tarix) AS first_prod_date,
    MAX(t.tarix) AS last_prod_date,
    DATEDIFF(day, MIN(t.tarix), MAX(t.tarix)) AS total_days,
    SUM(CASE WHEN t.sobe2 = 6 THEN tel.miqdar ELSE 0 END) AS total_produced
FROM sm_goods hm
JOIN sm_goods ym ON (ym.idn = hm.idn OR (ym.name LIKE 'YM-%' AND hm.name LIKE 'HM-%' AND SUBSTRING(ym.name, 4, LEN(ym.name)) = SUBSTRING(hm.name, 4, LEN(hm.name))))
JOIN sm_sob_trans_el tel ON tel.mal = ym.idn
JOIN sm_sob_trans t ON t.idn = tel.es_no
WHERE hm.class = 27 AND hm.muddet > 0 AND t.tesdiq = 1
GROUP BY hm.name, hm.muddet
HAVING DATEDIFF(day, MIN(t.tarix), MAX(t.tarix)) > 0 AND SUM(CASE WHEN t.sobe2 = 6 THEN tel.miqdar ELSE 0 END) > 0
ORDER BY total_produced DESC
"""
rows = query(sql)
for r in rows:
    prod = r['total_produced']
    days = r['total_days']
    db_muddet = r['db_muddet']
    mins_per_piece = (days * 24 * 60) / float(prod)
    print(f"Product: {r['product']}")
    print(f"Total Produced: {prod} over {days} days")
    print(f"Real Life Avg: {round(mins_per_piece, 2)} minutes per piece")
    print(f"Database Muddet value: {db_muddet}")
    print("-" * 40)
