import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    print("Checking qaliq for EKIN...")
    q1 = "SELECT TOP 10 s.idn, s.tarix, c.name as cname, e.miqdar, e.qaliq FROM sm_sifaris_form s JOIN sm_sifaris_form_el e ON e.es_no = s.idn JOIN sm_kontra c ON s.kontra = c.idn WHERE c.name LIKE '%EKIN%' ORDER BY s.tarix DESC"
    rows1 = query(q1)
    for r in rows1: print(r)

    print("\nChecking qaliq for Adonis...")
    q2 = "SELECT TOP 10 s.idn, s.tarix, c.name as cname, e.miqdar, e.qaliq FROM sm_sifaris_form s JOIN sm_sifaris_form_el e ON e.es_no = s.idn JOIN sm_kontra c ON s.kontra = c.idn WHERE c.name LIKE '%ADON%' ORDER BY s.tarix DESC"
    rows2 = query(q2)
    for r in rows2: print(r)

if __name__ == '__main__':
    check_logic()
