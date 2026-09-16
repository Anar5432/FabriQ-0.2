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
        SELECT TOP 5 idn, mal, miqdar, qaliq, sat_miq
        FROM sm_sif_sened_el
        WHERE sat_miq > 0
    """
    rows = query(q1)
    out.write(f"Rows with sat_miq > 0 in sm_sif_sened_el: {rows}\n")

    q2 = """
        SELECT TOP 5 idn, mal, miqdar, qaliq, sif_miq
        FROM sm_sifaris_form_el
        WHERE sif_miq > 0
    """
    rows2 = query(q2)
    out.write(f"Rows with sif_miq > 0 in sm_sifaris_form_el: {rows2}\n")

    with io.open("sat_miq.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
