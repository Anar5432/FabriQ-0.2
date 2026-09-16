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
        SELECT TOP 10 s.idn as invoice_id, s.sif_sen, e.mal, e.miqdar
        FROM sm_kontr_sat s
        JOIN sm_kontr_sat_el e ON s.idn = e.es_no
        WHERE s.sif_sen IS NOT NULL AND s.tarix >= '2026-06-01'
    """
    rows = query(q1)
    out.write(f"Invoices linked to sm_sif_sened: {rows}\n")

    with io.open("sif_sened_invoices.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
