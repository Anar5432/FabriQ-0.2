import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def run():
    # Let's check which table stores the orders
    res = query("SELECT COUNT(*) as c FROM sm_kontr_sat")
    print("Total sm_kontr_sat:", res[0]['c'])
    
    # Are there any rasenka records for sm_kontr_sat?
    # Usually, sm_kontr_sat.sen_no = sm_rasenka.sif_sen
    q1 = """
    SELECT TOP 15
        s.sen_no, s.tarix, s.kontra_name as customer, g.name as product_name, e.miqdar
    FROM sm_kontr_sat s
    JOIN sm_kontr_sat_el e ON s.idn = e.es_no
    JOIN sm_goods g ON e.mal = g.idn
    WHERE s.sen_no NOT IN (SELECT sif_sen FROM sm_rasenka WHERE sif_sen IS NOT NULL)
    ORDER BY s.tarix DESC
    """
    missing_orders = query(q1)
    
    print("\n--- Recent Orders missing Rasenka ---")
    for row in missing_orders:
        print(f"Order No: {row['sen_no']} | Date: {row['tarix']} | Customer: {row['customer']} | Product: {row['product_name']} | Qty: {row['miqdar']}")

if __name__ == '__main__':
    run()
