# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    q = "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN ('sm_kontr_sat', 'sm_sif_sened', 'sm_sifaris_form')"
    rows = query(q)
    for r in rows: out.write(f"{r['TABLE_NAME']} - {r['COLUMN_NAME']}\n")

    with io.open("cols_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
