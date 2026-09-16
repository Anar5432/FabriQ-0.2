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
        SELECT idn, 'sm_kontr_sat' as t FROM sm_kontr_sat WHERE idn = 22392
        UNION ALL
        SELECT idn, 'sm_sifaris_form' as t FROM sm_sifaris_form WHERE idn = 22392
        UNION ALL
        SELECT idn, 'sm_sif_sened' as t FROM sm_sif_sened WHERE idn = 22392
    """
    
    try:
        rows = query(q1)
        for r in rows: out.write(f"{r}\n")
    except Exception as e:
        out.write(f"Error: {e}\n")

    with io.open("prod_sif2.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
