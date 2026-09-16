import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    out.write("Checking qaliq for EKIN...\n")
    q1 = "SELECT TOP 10 s.idn, s.tarix, c.name as cname, e.miqdar, e.qaliq FROM sm_sifaris_form s JOIN sm_sifaris_form_el e ON e.es_no = s.idn JOIN sm_kontra c ON s.kontra = c.idn WHERE c.name LIKE '%EKIN%' ORDER BY s.tarix DESC"
    rows1 = query(q1)
    for r in rows1: out.write(f"{r}\n")

    out.write("\nChecking qaliq for Adonis...\n")
    q2 = "SELECT TOP 10 s.idn, s.tarix, c.name as cname, e.miqdar, e.qaliq FROM sm_sifaris_form s JOIN sm_sifaris_form_el e ON e.es_no = s.idn JOIN sm_kontra c ON s.kontra = c.idn WHERE c.name LIKE '%ADON%' ORDER BY s.tarix DESC"
    rows2 = query(q2)
    for r in rows2: out.write(f"{r}\n")

    with io.open("qaliq_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
