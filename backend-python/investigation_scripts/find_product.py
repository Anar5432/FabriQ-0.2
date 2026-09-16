# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    # 1. Search for the product
    q1 = """
        SELECT TOP 5 idn, name, class 
        FROM sm_goods 
        WHERE name LIKE '%ÖNLÜK AĞ İKİ CİBLİ (PARÇA)%' OR name LIKE '%14/0038%'
    """
    rows = query(q1)
    
    if rows:
        out.write("Found Products:\n")
        for r in rows:
            out.write(f"- ID: {r['idn']}, Name: {r['name']}, Class: {r['class']}\n")
            
            # 2. Get class info
            q2 = f"SELECT idn, name FROM sm_class WHERE idn = {r['class']}"
            class_info = query(q2)
            if class_info:
                out.write(f"  --> Class Name: {class_info[0]['name']} (ID: {class_info[0]['idn']})\n")
    else:
        out.write("Product not found.\n")

    with io.open("find_product.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
