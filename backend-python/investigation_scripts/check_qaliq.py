# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    out.write("--- MONEX (sm_sifaris_form) ---\n")
    q1 = """
        SELECT e.es_no, e.num, g.name, e.miqdar, e.qaliq, s.tarix
        FROM sm_sifaris_form_el e 
        JOIN sm_sifaris_form s ON e.es_no = s.idn
        JOIN sm_goods g ON e.mal = g.idn
        WHERE s.kontra_name LIKE '%MONEX%' AND s.tarix >= '2026-06-01'
        ORDER BY s.tarix DESC
    """
    try:
        rows = query(q1)
        for r in rows[:10]: out.write(f"{r}\n")
    except Exception as e:
        out.write(f"Error: {e}\n")

    out.write("\n--- ADONES (sm_sif_sened) ---\n")
    q2 = """
        SELECT e.es_no, e.num, g.name, e.miqdar, e.qaliq, s.tarix
        FROM sm_sif_sened_el e 
        JOIN sm_sif_sened s ON e.es_no = s.idn
        JOIN sm_goods g ON e.mal = g.idn
        WHERE s.kontra_name LIKE '%ADON%S%' AND s.tarix >= '2026-06-01'
        ORDER BY s.tarix DESC
    """
    try:
        rows = query(q2)
        for r in rows[:10]: out.write(f"{r}\n")
    except Exception as e:
        out.write(f"Error: {e}\n")

    with io.open("qaliq_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
