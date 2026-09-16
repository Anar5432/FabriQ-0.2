# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    # Take an order where qaliq > 0 and compare it to the current stock balance of that item
    q1 = """
        SELECT TOP 5 e.mal, e.qaliq, s.tarix
        FROM sm_sif_sened_el e
        JOIN sm_sif_sened s ON e.es_no = s.idn
        WHERE e.qaliq > 0 AND s.tarix >= '2026-01-01'
    """
    rows = query(q1)
    
    for r in rows:
        mal_id = r['mal']
        q2 = f"""
            SELECT SUM(miqdar) as total_stock
            FROM sm_mal_say
            WHERE mal = {mal_id}
        """
        stock = query(q2)[0]['total_stock']
        out.write(f"Product {mal_id}: Order qaliq={r['qaliq']} | True Stock={stock}\n")

    with io.open("qaliq_meaning.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
