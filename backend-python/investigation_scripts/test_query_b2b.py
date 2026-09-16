# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    cls = '(22, 24, 27, 31, 32, 34)'
    
    # 1. Official Invoices WITHOUT an order
    q1 = f"""
        SELECT COUNT(*) as c
        FROM sm_kontr_sat s WITH (NOLOCK)
        JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
        JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
        WHERE g.class IN {cls}
          AND s.sif_sen IS NULL AND s.sif_form IS NULL
          AND (e.qaliq > 0 OR s.tarix >= DATEADD(DAY, -60, GETDATE()))
    """
    
    # 2. Orders (Old)
    q2 = f"""
        SELECT COUNT(*) as c
        FROM sm_sifaris_form s WITH (NOLOCK)
        JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
        JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
        WHERE g.class IN {cls}
          AND (e.qaliq > 0 OR s.tarix >= DATEADD(DAY, -60, GETDATE()))
    """
    
    # 3. Orders (New)
    q3 = f"""
        SELECT COUNT(*) as c
        FROM sm_sif_sened s WITH (NOLOCK)
        JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
        JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
        WHERE g.class IN {cls}
          AND (e.qaliq > 0 OR s.tarix >= DATEADD(DAY, -60, GETDATE()))
    """
    
    out.write(f"Invoices without order: {query(q1)[0]['c']}\n")
    out.write(f"Old Orders: {query(q2)[0]['c']}\n")
    out.write(f"New Orders: {query(q3)[0]['c']}\n")

    with io.open("query_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
