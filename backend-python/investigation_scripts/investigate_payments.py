import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

with open('investigate_output2.txt', 'w', encoding='utf-8') as f:
    sql_cash = """
    SELECT 
        SUM(CASE WHEN qaime IS NOT NULL AND qaime != 0 THEN 1 ELSE 0 END) as with_qaime,
        SUM(CASE WHEN qaime IS NULL OR qaime = 0 THEN 1 ELSE 0 END) as without_qaime,
        COUNT(*) as total_rows
    FROM sm_kmd_el WITH (NOLOCK)
    """
    f.write("CASH PAYMENTS (sm_kmd_el):\n")
    f.write(str(query(sql_cash)) + "\n\n")

    sql_bank = """
    SELECT 
        SUM(CASE WHEN qaime IS NOT NULL AND qaime != 0 THEN 1 ELSE 0 END) as with_qaime,
        SUM(CASE WHEN qaime IS NULL OR qaime = 0 THEN 1 ELSE 0 END) as without_qaime,
        COUNT(*) as total_rows
    FROM sm_bank_od_el_el WITH (NOLOCK)
    """
    f.write("BANK PAYMENTS (sm_bank_od_el_el):\n")
    f.write(str(query(sql_bank)) + "\n\n")

    sql_kmd = """
    SELECT TOP 5
        k.idn, k.kontra, k.tarix, k.mebleg as Total_Header_Payment, e.odenen as Detail_Payment, e.qaime
    FROM sm_kmd k WITH (NOLOCK)
    JOIN sm_kmd_el e WITH (NOLOCK) ON k.idn = e.es_no
    WHERE (e.qaime IS NULL OR e.qaime = 0) AND k.kontra IS NOT NULL
    ORDER BY k.tarix DESC
    """
    f.write("Recent Cash Payments directly to Customer Account (No Invoice specified):\n")
    for r in query(sql_kmd):
        f.write(str(r) + "\n")
