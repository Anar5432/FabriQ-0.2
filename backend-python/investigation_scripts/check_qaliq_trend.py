# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    out.write("--- OLD ORDERS (Jan 2026) sm_sif_sened_el ---\n")
    q1 = """
        SELECT TOP 5 s.tarix, e.miqdar, e.qaliq
        FROM sm_sif_sened_el e
        JOIN sm_sif_sened s ON e.es_no = s.idn
        WHERE s.tarix >= '2026-01-01' AND s.tarix < '2026-02-01'
    """
    for r in query(q1): out.write(f"{r}\n")

    out.write("\n--- NEW ORDERS (June 2026) sm_sif_sened_el ---\n")
    q2 = """
        SELECT TOP 5 s.tarix, e.miqdar, e.qaliq
        FROM sm_sif_sened_el e
        JOIN sm_sif_sened s ON e.es_no = s.idn
        WHERE s.tarix >= '2026-06-01' AND s.tarix < '2026-07-01'
    """
    for r in query(q2): out.write(f"{r}\n")

    with io.open("qaliq_trend.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
