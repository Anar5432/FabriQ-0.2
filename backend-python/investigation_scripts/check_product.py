# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    # Find all recent orders for product 45689
    q1 = "SELECT * FROM sm_sifaris_form_el WHERE mal = 45689"
    out.write("In form_el:\n")
    for r in query(q1): out.write(f"{r}\n")
    
    q2 = "SELECT * FROM sm_kontr_sat_el WHERE mal = 45689"
    out.write("\nIn sat_el:\n")
    for r in query(q2): out.write(f"{r}\n")

    q3 = "SELECT * FROM sm_sifaris_qaime_el_el WHERE mal = 45689"
    out.write("\nIn qaime_el_el:\n")
    for r in query(q3): out.write(f"{r}\n")

    q4 = "SELECT * FROM sm_sifaris_el WHERE mal = 45689"
    out.write("\nIn sifaris_el:\n")
    for r in query(q4): out.write(f"{r}\n")

    with io.open("product_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
