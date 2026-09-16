# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    q = "SELECT TOP 10 name FROM sm_goods WHERE class = 22 AND name IS NOT NULL ORDER BY idn DESC"
    rows = query(q)
    for r in rows: out.write(f"{r['name']}\n")

    with io.open("class22_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
