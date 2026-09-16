# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    # In sm_sifaris_form_el, let's find if qaliq is ever > 0, or if sif_miq is related.
    q1 = """
        SELECT TOP 10 idn, mal, miqdar, qaliq, sif_miq
        FROM sm_sifaris_form_el
        WHERE miqdar > 0 AND miqdar != qaliq AND qaliq > 0
    """
    rows = query(q1)
    out.write(f"Rows with 0 < qaliq < miqdar in sm_sifaris_form_el: {rows}\n")

    with io.open("sifaris_part.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
