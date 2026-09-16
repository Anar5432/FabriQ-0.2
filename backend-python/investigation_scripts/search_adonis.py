import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    out.write("Searching for Adonis today...\n")
    q1 = "SELECT TOP 10 s.idn, s.sen_no, s.tarix, c.name as cname, g.name as pname, e.miqdar FROM sm_sifaris_form s JOIN sm_sifaris_form_el e ON e.es_no = s.idn JOIN sm_kontra c ON s.kontra = c.idn JOIN sm_goods g ON e.mal = g.idn WHERE c.name LIKE '%Adoni%' OR g.name LIKE '%Adoni%' ORDER BY s.tarix DESC"
    rows1 = query(q1)
    for r in rows1: out.write(f"Form: {r}\n")
    
    with io.open("adonis_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
