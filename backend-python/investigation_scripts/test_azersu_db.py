# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def test():
    out = io.StringIO()
    # Find AZƏRSU ASC
    q1 = "SELECT idn FROM sm_kontra WHERE name LIKE '%AZƏRSU%'"
    kontra = query(q1)
    if kontra:
        k_id = kontra[0]['idn']
        out.write(f"Kontra ID: {k_id}\n")
        
        q2 = f"""
        SELECT TOP 20 s.sen_no, g.name, e.miqdar
        FROM sm_sifaris_form s
        JOIN sm_sifaris_form_el e ON e.es_no = s.idn
        JOIN sm_goods g ON e.mal = g.idn
        WHERE s.kontra = {k_id} AND g.name LIKE '%01/0119%'
        ORDER BY s.tarix DESC
        """
        rows = query(q2)
        for r in rows:
            out.write(f"{r['sen_no']} | {r['name']} | {r['miqdar']}\n")
            
    with io.open("test_azersu_db.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    test()
