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
        SELECT TOP 10 idn, mal, miqdar, qaliq, ist_miqdar, ist_miq, sat_miq, ilk_miq
        FROM sm_sif_sened_el
        WHERE es_no = 4111
    """
    rows = query(q1)
    for r in rows:
        out.write(f"{r}\n")

    with io.open("sif_sened_miq_cols.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
