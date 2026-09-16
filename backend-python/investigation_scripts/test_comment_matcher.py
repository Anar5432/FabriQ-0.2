import pyodbc
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dashboard.erp_connector import query
from dashboard.comment_matcher import match_orders_to_transfers

def test_matcher():
    cls = "(27)" # isci geyimi
    sql = f"""
    SET NOCOUNT ON;
    SELECT
        s.idn AS order_id,
        s.sen_no,
        CONVERT(VARCHAR(10), s.tarix, 23) AS tarix,
        s.kontra AS company_id,
        s.kontra_name AS company_name,
        e.idn AS line_id,
        e.num AS line_num,
        g.idn AS product_id,
        g.name AS product_name,
        e.miqdar AS qty_ordered,
        e.qaliq AS qty_remaining
    FROM sm_kontr_sat s WITH (NOLOCK)
    JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    WHERE g.class IN {cls}
      AND (e.qaliq > 0 OR s.tarix >= DATEADD(DAY, -60, GETDATE()))
    ORDER BY s.tarix ASC, e.num;
    """
    base_lines = query(sql)
    
    # We just need distinct orders for matching
    distinct_orders = []
    seen = set()
    for b in base_lines:
        if b['order_id'] not in seen:
            seen.add(b['order_id'])
            distinct_orders.append(b)
            
    matches = match_orders_to_transfers(distinct_orders)
    
    print("=== FUZZY MATCH RESULTS ===")
    for order_id, transfers in matches.items():
        # find order
        order = next((o for o in distinct_orders if o['order_id'] == order_id), None)
        cname = order['company_name'] if order else "Unknown"
        print(f"\nOrder {order_id} ({cname}):")
        for t in transfers:
            print(f"  -> Transfer {t['sen_no']} (From: {t['sobe1']} To: {t['sobe2']}) Comment: {t['comment']}")

if __name__ == "__main__":
    test_matcher()
