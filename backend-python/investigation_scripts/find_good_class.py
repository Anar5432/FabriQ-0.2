# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    q1 = "SELECT idn, name FROM sm_good_class WHERE idn = 27"
    rows = query(q1)
    
    if rows:
        out.write(f"Class 27 is: {rows[0]['name']}\n")
    else:
        out.write("Class 27 not found in sm_good_class.\n")

    with io.open("find_good_class.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
