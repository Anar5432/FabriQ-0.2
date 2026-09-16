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
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'sm_sif_sened_el'
    """
    rows = query(q1)
    cols = [r['COLUMN_NAME'] for r in rows]
    out.write(f"Columns in sm_sif_sened_el: {cols}\n")

    q2 = """
        SELECT TOP 3 idn, mal, miqdar, qaliq
        FROM sm_sif_sened_el
        WHERE es_no = 4111
    """
    out.write(f"\nValues for es_no 4111: {query(q2)}\n")

    with io.open("sif_sened_cols.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
