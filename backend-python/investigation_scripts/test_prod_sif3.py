# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    q1 = """
        SELECT TOP 20 
            i.idn, i.sif_no,
            (SELECT COUNT(*) FROM sm_kontr_sat WHERE idn = i.sif_no) as is_sat,
            (SELECT COUNT(*) FROM sm_sif_sened WHERE idn = i.sif_no) as is_sif_sened,
            (SELECT COUNT(*) FROM sm_sifaris_form WHERE idn = i.sif_no) as is_sif_form
        FROM sm_good_ist i 
        WHERE i.sif_no IS NOT NULL AND i.sif_no IN (SELECT idn FROM sm_sif_sened)
        ORDER BY i.idn DESC
    """
    
    try:
        rows = query(q1)
        for r in rows: out.write(f"{r}\n")
    except Exception as e:
        out.write(f"Error: {e}\n")

    with io.open("prod_sif3.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
