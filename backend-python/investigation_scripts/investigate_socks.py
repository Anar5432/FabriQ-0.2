import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

with open('investigate_socks_production.txt', 'w', encoding='utf-8') as f:
    
    # Check what columns exist in sm_good_ist (Production Orders)
    try:
        sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_good_ist'"
        cols = [r['COLUMN_NAME'] for r in query(sql)]
        f.write(f"sm_good_ist columns: {cols}\n\n")
    except Exception as e:
        f.write(f"Error 1: {e}\n")

    # Look at recent socks production orders
    try:
        sql2 = """
        SELECT TOP 10 i.idn, i.tarix, i.qaime, i.sifaris, i.kontra, i.serh, 
                      e.mal, g.name as mal_name, e.miqdar
        FROM sm_good_ist i
        JOIN sm_good_ist_el e ON i.idn = e.es_no
        JOIN sm_goods g ON e.mal = g.idn
        WHERE g.class IN (21, 29, 30)
        ORDER BY i.tarix DESC
        """
        rows = query(sql2)
        f.write("Recent Socks Production Orders (sm_good_ist):\n")
        for r in rows:
            f.write(f"{r}\n")
    except Exception as e:
        f.write(f"Error 2: {e}\n")

    # Check for direct standard sales without a prior order, or wholesale (toptan)
    try:
        # Check sales orders (sm_kontr_sat)
        sql3 = """
        SELECT TOP 5 s.idn, s.tarix, s.kontra, s.serh, s.sifaris, c.name as customer
        FROM sm_kontr_sat s
        JOIN sm_kontr_sat_el e ON s.idn = e.es_no
        JOIN sm_goods g ON e.mal = g.idn
        LEFT JOIN sm_kontra c ON s.kontra = c.idn
        WHERE g.class IN (21, 29, 30)
        ORDER BY s.tarix DESC
        """
        rows = query(sql3)
        f.write("\nRecent Socks Sales Orders (sm_kontr_sat):\n")
        for r in rows:
            f.write(f"{r}\n")
    except Exception as e:
        f.write(f"Error 3: {e}\n")
