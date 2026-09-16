# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    out.write("Checking product class for MONEX items...\n")
    q = "SELECT idn, name, class FROM sm_goods WHERE name LIKE '%0070 L%CRASIZ%'"
    rows = query(q)
    for r in rows: out.write(f"{r}\n")

    with io.open("monex_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
