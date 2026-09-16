# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def test():
    out = io.StringIO()
    q = "SELECT idn, name, class FROM sm_goods WHERE name LIKE 'YM-BETEX/01/0119%'"
    rows = query(q)
    for r in rows:
        out.write(f"ID: {r['idn']} | Name: {r['name']} | Class: {r['class']}\n")
    with io.open("test_ym.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    test()
