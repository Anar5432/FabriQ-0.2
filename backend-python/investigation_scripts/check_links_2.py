# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    q = "SELECT TOP 20 idn, sif_sen, sif_form FROM sm_kontr_sat WHERE sif_sen IS NOT NULL OR sif_form IS NOT NULL ORDER BY idn DESC"
    rows = query(q)
    for r in rows: out.write(f"{r}\n")

    with io.open("links_out_2.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
