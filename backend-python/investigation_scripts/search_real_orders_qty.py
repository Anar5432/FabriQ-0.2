import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def search_qty():
    out = io.StringIO()
    out.write("--- Searching for specific quantities and strings ---\n")
    
    # 1. sm_sifaris_form_el (Order Lines)
    try:
        q1 = """
        SELECT e.idn, e.es_no, e.miqdar, g.name as product_name
        FROM sm_sifaris_form_el e
        JOIN sm_goods g ON e.mal = g.idn
        WHERE e.miqdar IN (20, 27) OR g.name LIKE '%Adonis%' OR g.name LIKE '%EKIN%'
        ORDER BY e.idn DESC
        """
        records = query(q1)
        out.write(f"\n--- sm_sifaris_form_el ({len(records)} matching records) ---\n")
        # Just grab the top 15 matches to not flood the file
        for r in records[:15]:
            out.write(f"Line: {r}\n")
    except Exception as e:
        out.write(f"Error in sm_sifaris_form_el: {e}\n")
        
    # 2. sm_sifaris_form (Headers for the names)
    try:
        q2 = """
        SELECT s.idn, s.sen_no, s.tarix, s.ins_user, c.name as customer_name
        FROM sm_sifaris_form s
        LEFT JOIN sm_kontra c ON s.kontra = c.id
        WHERE c.name LIKE '%EKIN%' OR c.name LIKE '%Aytekin%' OR c.name LIKE '%Yusif%'
           OR s.ins_user LIKE '%Aytekin%' OR s.ins_user LIKE '%Yusif%'
        ORDER BY s.tarix DESC
        """
        records = query(q2)
        out.write(f"\n--- sm_sifaris_form matches by name ({len(records)} records) ---\n")
        for r in records[:15]:
            out.write(f"Header: {r}\n")
    except Exception as e:
        out.write(f"Error in sm_sifaris_form headers: {e}\n")

    # 3. What about mob_sifaris / mob_sifaris_el?
    try:
        q3 = """
        SELECT s.idn, s.tarix, s.ins_user, c.name as customer_name, e.miqdar, g.name as product_name
        FROM mob_sifaris s
        JOIN mob_sifaris_el e ON s.idn = e.es_no
        LEFT JOIN sm_kontra c ON s.kontra = c.id
        JOIN sm_goods g ON e.mal = g.idn
        WHERE e.miqdar IN (20, 27) OR c.name LIKE '%EKIN%' OR c.name LIKE '%Aytekin%' 
           OR g.name LIKE '%Adonis%'
        ORDER BY s.tarix DESC
        """
        records = query(q3)
        out.write(f"\n--- mob_sifaris matches ({len(records)} records) ---\n")
        for r in records[:15]:
            out.write(f"Mob Sifaris: {r}\n")
    except Exception as e:
        pass

    with io.open("search_qty.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    search_qty()
