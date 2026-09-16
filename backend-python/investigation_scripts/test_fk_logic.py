# -*- coding: utf-8 -*-
import sys
import os
import django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query
from dashboard.queries import get_sector_rules

def test_step_1_to_3():
    print("Testing Foreign Key Tracing (Steps 1, 2, 3)...\n")
    sector = 'isci'
    rules = get_sector_rules(sector)
    cls_cond = rules['class_condition']
    
    # Let's get recent orders
    sql = f"""
        SET NOCOUNT ON;
        SELECT TOP 50
            s.idn AS order_id,
            s.sen_no,
            s.yekun AS order_total,
            CONVERT(VARCHAR(10), s.tarix, 23) AS tarix,
            s.kontra AS company_id,
            c.name AS company_name,
            e.idn AS line_id,
            e.num AS line_num,
            g.idn AS product_id,
            g.name AS product_name,
            e.miqdar AS qty_ordered,
            ist.idn AS prod_doc_id
        FROM sm_sifaris_form s WITH (NOLOCK)
        JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
        LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
        JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
        LEFT JOIN sm_good_ist ist WITH (NOLOCK) ON ist.sif_no = s.idn
        WHERE {cls_cond}
          AND s.tarix >= DATEADD(DAY, -60, GETDATE())
        ORDER BY s.tarix DESC;
    """
    orders = query(sql)
    print(f"Found {len(orders)} order lines (from sm_sifaris_form).")
    
    # Let's check how many have production documents
    with_prod = [o for o in orders if o['prod_doc_id']]
    print(f"Orders WITH production documents (sm_good_ist): {len(with_prod)}")
    
    # Check if son_faza is populated for corab items
    sql_check_faza = """
        SELECT TOP 10 ie.idn, ie.mal, ie.son_faza, g.name
        FROM sm_good_ist_el ie WITH (NOLOCK)
        JOIN sm_goods g WITH (NOLOCK) ON ie.mal = g.idn
        WHERE g.class IN (21, 29, 30) AND ie.son_faza IS NOT NULL AND ie.son_faza > 0
    """
    fazas = query(sql_check_faza)
    print(f"\nChecking son_faza for Corab (Found {len(fazas)}):")
    for f in fazas:
        print(f"  - Element: {f['idn']} | mal: {f['mal']} ({f['name']}) | son_faza: {f['son_faza']}")

if __name__ == '__main__':
    test_step_1_to_3()
