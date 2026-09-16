import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django; django.setup()
from dashboard.erp_connector import query

print("TESTING OVERALL BALANCES")

sql = """
-- Let's calculate balances for ALL YM- items and show the top 5 with highest balance somewhere
SELECT TOP 5
    g.name AS product_name,
    dept.name AS dept_name,
    ISNULL(ins.qty_in, 0) - ISNULL(outs.qty_out, 0) AS balance
FROM sm_goods g
JOIN (
    SELECT t.sobe2 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_in
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1
    GROUP BY t.sobe2, tel.mal
) ins ON g.idn = ins.mal
LEFT JOIN sm_depo dept ON ins.dept_id = dept.idn
LEFT JOIN (
    SELECT t.sobe1 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_out
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1 AND t.sobe1 IS NOT NULL
    GROUP BY t.sobe1, tel.mal
) outs ON ins.dept_id = outs.dept_id AND ins.mal = outs.mal
WHERE g.class = 27
  AND (ISNULL(ins.qty_in, 0) - ISNULL(outs.qty_out, 0)) > 0
ORDER BY balance DESC;
"""
rows = query(sql)
for r in rows:
    print(r)
