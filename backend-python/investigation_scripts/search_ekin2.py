import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    out.write("Searching for EKIN in sm_sifaris_form today or last few days...\n")
    q1 = "SELECT TOP 10 s.idn, s.sen_no, s.tarix, c.name as cname, g.name as pname, e.miqdar FROM sm_sifaris_form s JOIN sm_sifaris_form_el e ON e.es_no = s.idn JOIN sm_kontra c ON s.kontra = c.idn JOIN sm_goods g ON e.mal = g.idn WHERE c.name LIKE '%EKIN%' ORDER BY s.tarix DESC"
    rows1 = query(q1)
    for r in rows1: out.write(f"Form: {r}\n")

    out.write("\nSearching for EKIN in sm_kontr_sat...\n")
    q2 = "SELECT TOP 10 s.idn, s.sen_no, s.tarix, c.name as cname, g.name as pname, e.miqdar FROM sm_kontr_sat s JOIN sm_kontr_sat_el e ON e.es_no = s.idn JOIN sm_kontra c ON s.kontra = c.idn JOIN sm_goods g ON e.mal = g.idn WHERE c.name LIKE '%EKIN%' ORDER BY s.tarix DESC"
    rows2 = query(q2)
    for r in rows2: out.write(f"Sat: {r}\n")
    
    with io.open("ekin_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
