import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

sql = """
SET NOCOUNT ON;
SELECT TOP 5
    s.kontra_name,
    s.sen_no AS Sifaris_No,
    s.tarix,
    s.tam_yek AS Umumi_Mebleg,
    ISNULL(b.odenen, 0) + ISNULL(c.odenen, 0) AS Odenilen_Mebleg
FROM sm_kontr_sat s
LEFT JOIN (
    SELECT qaime, SUM(odenen) as odenen FROM sm_bank_od_el_el GROUP BY qaime
) b ON s.idn = b.qaime
LEFT JOIN (
    SELECT qaime, SUM(odenen) as odenen FROM sm_kmd_el GROUP BY qaime
) c ON s.idn = c.qaime
WHERE (ISNULL(b.odenen, 0) + ISNULL(c.odenen, 0)) > 0
ORDER BY s.tarix DESC
"""

rows = query(sql)
with open('paid_examples.txt', 'w', encoding='utf-8') as f:
    for row in rows:
        f.write(f"Customer: {row['kontra_name']} | Order: {row['Sifaris_No']} | Total: {row['Umumi_Mebleg']} | Paid: {row['Odenilen_Mebleg']}\n")
