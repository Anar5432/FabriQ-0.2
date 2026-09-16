# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    # First, get the product ID for HM-BETEX 05/0007 POLO R-50
    q_prod = "SELECT idn FROM sm_goods WHERE name LIKE '%05/0007 POLO%' AND name LIKE '%R-50%'"
    prods = query(q_prod)
    if not prods:
        out.write("Product not found!\n")
        
        with io.open("table_out.txt", "w", encoding="utf-8") as f:
            f.write(out.getvalue())
        return
        
    p_id = prods[0]['idn']
    out.write(f"Product ID is {p_id}\n")
    
    # We want to find tables that have a column for product and quantity
    out.write("Searching all tables for this product with miqdar=9...\n")
    
    tables_to_check = [
        ('sm_sifaris_el', 'es_no', 'mal', 'miqdar'),
        ('sm_sifaris_form_el', 'es_no', 'mal', 'miqdar'),
        ('sm_sifaris_qaime_el_el', 'es_no', 'mal', 'miqdar'),
        ('sm_kontr_sat_el', 'es_no', 'mal', 'miqdar'),
        ('mob_sifaris_el', 'es_no', 'mal', 'miqdar'),
        ('sm_sifaris_qaime_el', 'es_no', 'mal', 'miqdar'),
        ('sm_kontr_sat_ist_el', 'es_no', 'mal', 'miqdar')
    ]
    
    for tbl, es_col, mal_col, miq_col in tables_to_check:
        try:
            q = f"SELECT * FROM {tbl} WHERE {mal_col} = {p_id} AND {miq_col} = 9"
            rows = query(q)
            if rows:
                out.write(f"\nFound in {tbl}!\n")
                for r in rows: out.write(f"{r}\n")
        except Exception as e:
            out.write(f"Error checking {tbl}: {e}\n")

    with io.open("table_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
