import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    out.write("Checking sm_sifaris_form top 20 recent rows...\n")
    q = "SELECT TOP 20 s.idn, s.sen_no, s.tarix, c.name as customer, e.miqdar FROM sm_sifaris_form s JOIN sm_sifaris_form_el e ON e.es_no = s.idn LEFT JOIN sm_kontra c ON s.kontra = c.idn ORDER BY s.tarix DESC, s.idn DESC"
    rows = query(q)
    for r in rows: out.write(f"{r}\n")

    with io.open("top_form.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
