import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    q = "SELECT TOP 10 s.tarix, e.miqdar, e.qaliq, e.sif_miq, g.name FROM sm_sifaris_form_el e JOIN sm_sifaris_form s ON e.es_no = s.idn JOIN sm_goods g ON e.mal = g.idn WHERE e.qaliq = 0 ORDER BY e.idn DESC"
    rows = query(q)
    out.write("Recent Sifaris Form EL with qaliq = 0:\n")
    for r in rows:
        out.write(f"{r}\n")

    q2 = "SELECT TOP 10 s.tarix, e.miqdar, e.qaliq, e.sif_miq, g.name FROM sm_sifaris_form_el e JOIN sm_sifaris_form s ON e.es_no = s.idn JOIN sm_goods g ON e.mal = g.idn WHERE e.qaliq > 0 ORDER BY e.idn DESC"
    rows2 = query(q2)
    out.write("\nRecent Sifaris Form EL with qaliq > 0:\n")
    for r in rows2:
        out.write(f"{r}\n")
        
    with io.open("qaliq_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
