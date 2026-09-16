import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    out.write("Checking sm_sifaris_qaime for 004111 and 004198...\n")
    q = "SELECT s.idn, s.sen_no, s.tarix, c.name, e.mal, e.miqdar FROM sm_sifaris_qaime s JOIN sm_sifaris_qaime_el e ON e.es_no = s.idn LEFT JOIN sm_kontra c ON s.kontra = c.idn WHERE s.sen_no IN ('004111', '004198', '4111', '4198') OR s.idn IN (4111, 4198)"
    rows = query(q)
    for r in rows: out.write(f"{r}\n")

    with io.open("qaime_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
