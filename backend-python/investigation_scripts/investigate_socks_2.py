import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

with open('investigate_socks_production_2.txt', 'w', encoding='utf-8') as f:
    try:
        sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_kontr_sat'"
        cols = [r['COLUMN_NAME'] for r in query(sql)]
        f.write(f"sm_kontr_sat columns: {cols}\n\n")
    except Exception as e:
        f.write(f"Error: {e}\n")

    try:
        # Check standard production (sif_no is null or not)
        sql2 = """
        SELECT TOP 10 i.idn, i.tarix, i.sif_no, i.sif_name, 
                      g.name as mal_name, e.miqdar
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

    try:
        # Check how standard socks sales are recorded
        sql3 = """
        SELECT TOP 5 s.idn, s.tarix, s.kontra, s.serh, c.name as customer
        FROM sm_kontr_sat s
        LEFT JOIN sm_kontra c ON s.kontra = c.idn
        JOIN sm_kontr_sat_el e ON s.idn = e.es_no
        JOIN sm_goods g ON e.mal = g.idn
        WHERE g.class IN (21, 29, 30)
        ORDER BY s.tarix DESC
        """
        rows = query(sql3)
        f.write("\nRecent Socks Sales Orders (sm_kontr_sat):\n")
        for r in rows:
            f.write(f"{r}\n")
    except Exception as e:
        f.write(f"Error 3: {e}\n")
