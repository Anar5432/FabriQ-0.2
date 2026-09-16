# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def test():
    out = io.StringIO()
    # Find Document 022343
    q1 = """
        SELECT s.sen_no, s.tarix, s.kontra_name, g.name AS product_name, e.miqdar
        FROM sm_kontr_sat s
        JOIN sm_kontr_sat_el e ON e.es_no = s.idn
        JOIN sm_goods g ON e.mal = g.idn
        WHERE s.sen_no = '022343'
        
        UNION ALL
        
        SELECT s.sen_no, s.tarix, '' AS kontra_name, g.name AS product_name, e.miqdar
        FROM sm_sifaris_form s
        JOIN sm_sifaris_form_el e ON e.es_no = s.idn
        JOIN sm_goods g ON e.mal = g.idn
        WHERE s.sen_no = '022343'
        
        UNION ALL
        
        SELECT s.sen_no, s.tarix, '' AS kontra_name, g.name AS product_name, e.miqdar
        FROM sm_sif_sened s
        JOIN sm_sif_sened_el e ON e.es_no = s.idn
        JOIN sm_goods g ON e.mal = g.idn
        WHERE s.sen_no = '022343'
    """
    rows = query(q1)
    if rows:
        for r in rows:
            out.write(f"{r['sen_no']} | {r['tarix']} | {r['kontra_name']} | {r['product_name']} | {r['miqdar']}\n")
    else:
        out.write("Doc 022343 not found.\n")
            
    with io.open("test_db_doc.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    test()
