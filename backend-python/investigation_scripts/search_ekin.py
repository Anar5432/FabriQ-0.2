import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    print("Searching for EKIN in sm_sifaris_form today or last few days...")
    q1 = "SELECT TOP 10 s.idn, s.sen_no, s.tarix, c.name as cname, g.name as pname, e.miqdar FROM sm_sifaris_form s JOIN sm_sifaris_form_el e ON e.es_no = s.idn JOIN sm_kontra c ON s.kontra = c.idn JOIN sm_goods g ON e.mal = g.idn WHERE c.name LIKE '%EKIN%' ORDER BY s.tarix DESC"
    rows1 = query(q1)
    for r in rows1: print("Form:", r)

    print("\nSearching for EKIN in sm_kontr_sat...")
    q2 = "SELECT TOP 10 s.idn, s.sen_no, s.tarix, c.name as cname, g.name as pname, e.miqdar FROM sm_kontr_sat s JOIN sm_kontr_sat_el e ON e.es_no = s.idn JOIN sm_kontra c ON s.kontra = c.idn JOIN sm_goods g ON e.mal = g.idn WHERE c.name LIKE '%EKIN%' ORDER BY s.tarix DESC"
    rows2 = query(q2)
    for r in rows2: print("Sat:", r)

if __name__ == '__main__':
    check_logic()
