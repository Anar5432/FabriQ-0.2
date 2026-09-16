# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    q = "SELECT DISTINCT g.class, v.class_name FROM sm_goods g LEFT JOIN sm_goods_v v ON g.idn = v.idn WHERE g.class IS NOT NULL ORDER BY g.class"
    rows = query(q)
    for r in rows: out.write(f"{r}\n")

    with io.open("find_classes_out3.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
