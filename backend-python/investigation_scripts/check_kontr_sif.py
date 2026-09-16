# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    out.write("Checking sm_kontr_sif_sat...\n")
    q1 = "SELECT TOP 10 s.idn, s.sen_no, s.tarix, c.name, e.miqdar FROM sm_kontr_sif_sat s JOIN sm_kontr_sif_sat_el e ON e.es_no = s.idn LEFT JOIN sm_kontra c ON s.kontra = c.idn WHERE s.sen_no LIKE '%4111%' OR c.name LIKE '%ADONI%'"
    rows = query(q1)
    for r in rows: out.write(f"{r}\n")

    out.write("\nChecking recent orders in sm_kontr_sif_sat...\n")
    q2 = "SELECT TOP 5 s.idn, s.sen_no, s.tarix, c.name, e.miqdar FROM sm_kontr_sif_sat s JOIN sm_kontr_sif_sat_el e ON e.es_no = s.idn LEFT JOIN sm_kontra c ON s.kontra = c.idn ORDER BY s.tarix DESC"
    rows2 = query(q2)
    for r in rows2: out.write(f"{r}\n")

    with io.open("kontr_sif_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
