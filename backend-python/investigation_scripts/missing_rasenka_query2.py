import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def run():
    q1 = """
    SELECT TOP 20
        s.sen_no, s.tarix, s.kontra_name as customer, g.name as product_name, e.miqdar
    FROM sm_kontr_sat s
    JOIN sm_kontr_sat_el e ON s.idn = e.es_no
    JOIN sm_goods g ON e.mal = g.idn
    WHERE s.sen_no NOT IN (SELECT sif_sen FROM sm_rasenka WHERE sif_sen IS NOT NULL)
    ORDER BY s.tarix DESC, s.idn DESC
    """
    missing_orders = query(q1)
    
    with io.open("missing_orders.txt", "w", encoding="utf-8") as f:
        f.write("--- Recent Orders missing Rasenka ---\n")
        for row in missing_orders:
            f.write(f"Order No: {row['sen_no']} | Date: {row['tarix']} | Customer: {row['customer']} | Product: {row['product_name']} | Qty: {row['miqdar']}\n")

if __name__ == '__main__':
    run()
