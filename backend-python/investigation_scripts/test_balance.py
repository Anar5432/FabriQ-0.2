import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django; django.setup()
from dashboard.erp_connector import query

print("TESTING BALANCE CALCULATION FOR A SPECIFIC PRODUCT")

sql = """
-- Let's take a specific YM- product and calculate its department balances
DECLARE @mal INT = (SELECT TOP 1 idn FROM sm_goods WHERE name = 'YM-BETEX/08/0063 T-SHİRT OVERSİZE QARA KİŞİ R-M (P');

SELECT 
    dept.idn AS dept_id,
    dept.name AS dept_name,
    ISNULL(ins.qty_in, 0) AS total_in,
    ISNULL(outs.qty_out, 0) AS total_out,
    ISNULL(ins.qty_in, 0) - ISNULL(outs.qty_out, 0) AS balance
FROM sm_depo dept
LEFT JOIN (
    SELECT t.sobe2 AS dept_id, SUM(tel.miqdar) AS qty_in
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1 AND tel.mal = @mal
    GROUP BY t.sobe2
) ins ON dept.idn = ins.dept_id
LEFT JOIN (
    SELECT t.sobe1 AS dept_id, SUM(tel.miqdar) AS qty_out
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1 AND tel.mal = @mal AND t.sobe1 IS NOT NULL
    GROUP BY t.sobe1
) outs ON dept.idn = outs.dept_id
WHERE ISNULL(ins.qty_in, 0) > 0 OR ISNULL(outs.qty_out, 0) > 0
ORDER BY dept_id;
"""

rows = query(sql)
print("Balances for YM-BETEX/08/0063 T-SHİRT OVERSİZE QARA KİŞİ R-M (P :")
for r in rows:
    print(r)
