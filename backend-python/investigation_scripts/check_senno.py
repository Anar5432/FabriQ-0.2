import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    out.write("Checking sm_sifaris_form for sen_no 004111...\n")
    q = "SELECT s.idn, s.sen_no, s.tarix, c.name, e.miqdar FROM sm_sifaris_form s JOIN sm_sifaris_form_el e ON e.es_no = s.idn LEFT JOIN sm_kontra c ON s.kontra = c.idn WHERE s.sen_no LIKE '%4111%'"
    rows = query(q)
    for r in rows: out.write(f"{r}\n")

    with io.open("senno_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
