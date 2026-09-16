import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

with open('investigate_negative_paid.txt', 'w', encoding='utf-8') as f:
    # Check SOCAR H.ƏLİYEV (ID 41) in sm_borc
    sql = """
    SELECT tarix, nov, mebleg, yekun, serh
    FROM sm_borc
    WHERE kontra = 41
    ORDER BY tarix ASC
    """
    rows = query(sql)
    for r in rows:
        f.write(f"{r}\n")
    
    f.write("\n---\n")
    sql_sat = """
    SELECT tarix, tam_yek, status
    FROM sm_kontr_sat
    WHERE kontra = 41
    ORDER BY tarix ASC
    """
    rows2 = query(sql_sat)
    for r in rows2:
        f.write(f"{r}\n")

