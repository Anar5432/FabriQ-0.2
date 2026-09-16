# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    out.write("--- sm_kontr_sat_el ---\n")
    q1 = """
        SELECT TOP 10 s.tarix, e.miqdar, e.qaliq
        FROM sm_kontr_sat_el e
        JOIN sm_kontr_sat s ON e.es_no = s.idn
        WHERE s.tarix < '2026-05-01' AND s.tarix > '2026-01-01'
    """
    rows = query(q1)
    for r in rows:
        out.write(f"{r}\n")

    with io.open("kontr_qaliq.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
