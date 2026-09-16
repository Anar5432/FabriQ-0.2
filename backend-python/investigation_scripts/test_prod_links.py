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
        SELECT TOP 10 
            i.idn, i.sif_no, i.sif_sen, i.sif_form 
        FROM sm_good_ist i 
        WHERE i.sif_sen IS NOT NULL OR i.sif_form IS NOT NULL 
        ORDER BY i.idn DESC
    """
    
    try:
        rows = query(q1)
        for r in rows: out.write(f"Prod: {r}\n")
    except Exception as e:
        out.write(f"Error: {e}\n")

    with io.open("prod_links.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
