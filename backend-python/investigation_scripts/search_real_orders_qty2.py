import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def search_qty():
    # Fix the join to use idn for sm_kontra
    print("--- Searching sm_sifaris_form (Pending Orders) ---")
    try:
        q = """
        SELECT s.idn as header_id, s.tarix, s.ins_user as username, c.name as customer_name, e.miqdar, g.name as product_name
        FROM sm_sifaris_form s
        LEFT JOIN sm_kontra c ON s.kontra = c.idn
        JOIN sm_sifaris_form_el e ON s.idn = e.es_no
        JOIN sm_goods g ON e.mal = g.idn
        WHERE (e.miqdar IN (20, 27) AND (c.name LIKE '%EKIN%' OR g.name LIKE '%Adonis%'))
           OR c.name LIKE '%EKIN SMART%'
        ORDER BY s.tarix DESC
        """
        records = query(q)
        for r in records:
            print(f"MATCH: {r}")
    except Exception as e:
        print(f"Error: {e}")
        
    print("\n--- Searching sm_kontr_sif_sat (Sales Orders) ---")
    try:
        q = """
        SELECT s.idn as header_id, s.tarix, s.ins_user as username, s.kontra_name as customer_name, e.miqdar, g.name as product_name
        FROM sm_kontr_sif_sat s
        JOIN sm_kontr_sif_sat_el e ON s.idn = e.es_no
        JOIN sm_goods g ON e.mal = g.idn
        WHERE (e.miqdar IN (20, 27) AND (s.kontra_name LIKE '%EKIN%' OR g.name LIKE '%Adonis%'))
           OR s.kontra_name LIKE '%EKIN SMART%'
        ORDER BY s.tarix DESC
        """
        records = query(q)
        for r in records:
            print(f"MATCH: {r}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- Searching sm_kontr_sat (Invoices - Current Dashboard Source) ---")
    try:
        q = """
        SELECT s.idn as header_id, s.tarix, s.ins_user as username, s.kontra_name as customer_name, e.miqdar, g.name as product_name
        FROM sm_kontr_sat s
        JOIN sm_kontr_sat_el e ON s.idn = e.es_no
        JOIN sm_goods g ON e.mal = g.idn
        WHERE (e.miqdar IN (20, 27) AND (s.kontra_name LIKE '%EKIN%' OR g.name LIKE '%Adonis%'))
           OR s.kontra_name LIKE '%EKIN SMART%'
        ORDER BY s.tarix DESC
        """
        records = query(q)
        for r in records:
            print(f"MATCH: {r}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    search_qty()
