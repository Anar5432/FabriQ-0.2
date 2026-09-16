# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def test():
    out = io.StringIO()
    # Find all distinct classes for BETEX products
    q = "SELECT DISTINCT class, (SELECT name FROM sm_good_class WHERE idn = class) as class_name FROM sm_goods WHERE name LIKE '%BETEX%'"
    rows = query(q)
    for r in rows:
        out.write(f"Class: {r['class']} | Name: {r['class_name']}\n")
    with io.open("test_betex.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    test()
