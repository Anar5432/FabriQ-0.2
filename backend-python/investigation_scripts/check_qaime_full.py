import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    out.write("Checking sm_sifaris_qaime for 004111...\n")
    q = "SELECT TOP 10 s.idn, s.sen_no, s.tarix, c.name, g.name, el.sif_miq, el.miqdar FROM sm_sifaris_qaime s JOIN sm_sifaris_qaime_el_el el ON el.es_no = s.idn JOIN sm_goods g ON el.mal = g.idn LEFT JOIN sm_kontra c ON s.kontra = c.idn WHERE s.sen_no = '004111' OR s.idn = 4111"
    rows = query(q)
    for r in rows: out.write(f"{r}\n")

    with io.open("qaime_full.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
