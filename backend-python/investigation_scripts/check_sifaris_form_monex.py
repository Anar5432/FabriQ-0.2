# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    q2 = """
        SELECT TOP 10 e.idn, e.mal, e.miqdar, e.qaliq, e.sif_miq, s.tarix
        FROM sm_sifaris_form_el e
        JOIN sm_sifaris_form s ON e.es_no = s.idn
        LEFT JOIN sm_kontra c ON s.kontra = c.idn
        WHERE c.name LIKE '%MONEX%' AND s.tarix >= '2026-06-01'
    """
    try:
        rows = query(q2)
        for r in rows:
            out.write(f"{r}\n")
    except Exception as e:
        out.write(f"Error: {e}\n")

    with io.open("sifaris_form_monex.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
