# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    out.write("--- OLDER sm_sif_sened_el (New System) ---\n")
    q1 = """
        SELECT TOP 10 s.tarix, e.miqdar, e.qaliq, e.sat_miq, s.kontra_name
        FROM sm_sif_sened_el e
        JOIN sm_sif_sened s ON e.es_no = s.idn
        WHERE s.tarix < '2026-05-01' AND s.tarix > '2026-01-01'
    """
    rows = query(q1)
    for r in rows:
        out.write(f"{r}\n")

    out.write("\n--- OLDER sm_sifaris_form_el (Old System) ---\n")
    q2 = """
        SELECT TOP 10 s.tarix, e.miqdar, e.qaliq, s.kontra
        FROM sm_sifaris_form_el e
        JOIN sm_sifaris_form s ON e.es_no = s.idn
        WHERE s.tarix < '2026-05-01' AND s.tarix > '2026-01-01'
    """
    rows2 = query(q2)
    for r in rows2:
        out.write(f"{r}\n")

    out.write("\n--- sm_sif_sened_el QALIQ > 0 ---\n")
    q3 = "SELECT COUNT(*) as count FROM sm_sif_sened_el WHERE qaliq > 0"
    out.write(f"Count of rows with qaliq > 0: {query(q3)}\n")

    out.write("\n--- sm_sifaris_form_el QALIQ > 0 ---\n")
    q4 = "SELECT COUNT(*) as count FROM sm_sifaris_form_el WHERE qaliq > 0"
    out.write(f"Count of rows with qaliq > 0: {query(q4)}\n")

    with io.open("old_qaliq.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
