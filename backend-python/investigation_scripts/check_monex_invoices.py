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
        SELECT s.idn as invoice_id, s.sif_form, e.mal, e.miqdar
        FROM sm_kontr_sat s
        JOIN sm_kontr_sat_el e ON s.idn = e.es_no
        WHERE s.sif_form IN (
            SELECT s.idn
            FROM sm_sifaris_form s
            LEFT JOIN sm_kontra c ON s.kontra = c.idn
            WHERE c.name LIKE '%MONEX%' AND s.tarix >= '2026-06-01'
        )
    """
    rows = query(q1)
    out.write(f"Invoices linked to recent Monex orders: {rows}\n")

    with io.open("monex_invoices.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
