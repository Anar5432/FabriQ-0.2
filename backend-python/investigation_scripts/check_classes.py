# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    q = "SELECT c.idn, c.name FROM sm_class c WHERE c.idn IN (15, 32, 6, 27, 21, 18, 10, 31, 20, 28)"
    rows = query(q)
    for r in rows: out.write(f"{r}\n")

    with io.open("classes_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
