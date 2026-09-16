# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    # Check if 004111 is in sm_sifaris
    q1 = "SELECT idn, sen_no, tarix FROM sm_sifaris WHERE sen_no = '004111' OR sen_no = '4111'"
    out.write("In sm_sifaris:\n")
    for r in query(q1): out.write(f"{r}\n")
    
    with io.open("sifaris_table_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
