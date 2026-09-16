# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    q = "SELECT class, class_name, COUNT(*) as product_count FROM sm_goods_v GROUP BY class, class_name ORDER BY class"
    rows = query(q)
    for r in rows: out.write(f"{r}\n")

    with io.open("find_classes_out2.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
