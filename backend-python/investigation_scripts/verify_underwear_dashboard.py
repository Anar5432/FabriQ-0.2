import os
import sys
import django
import json

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders
from dashboard.erp_connector import query
from django.core.cache import cache

def main():
    print("Clearing cache...")
    cache.clear()
    
    print("Fetching underwear orders via get_orders()...")
    orders_data = get_orders('underwear')
    
    print(f"Number of orders/lines returned: {len(orders_data)}")
    
    if isinstance(orders_data, dict):
        if 'companies' in orders_data:
            companies = orders_data['companies']
            print(f"Total companies: {len(companies)}")
            total_orders = sum(len(c.get('orders', [])) for c in companies)
            print(f"Total orders across all companies: {total_orders}")
            print("First company and its first 2 orders:")
            if companies:
                c0 = companies[0]
                print(f"\\nCompany: {c0.get('name')}")
                for idx, order in enumerate(c0.get('orders', [])[:2]):
                    print(f"  Order {idx+1}:")
                    print(json.dumps(order, indent=4, ensure_ascii=False))
        else:
            print("Keys in orders_data:", orders_data.keys())
            
    elif isinstance(orders_data, list):
        print(f"Total orders: {len(orders_data)}")
        for idx, order in enumerate(orders_data[:2]):
            print(f"\\nDashboard Order {idx+1}:")
            print(json.dumps(order, indent=2, ensure_ascii=False))
    print("\\n--- Checking for Order 3299 in Dashboard Data ---")
    found_dashboard = []
    if isinstance(orders_data, dict) and 'companies' in orders_data:
        for company in orders_data['companies']:
            for order in company.get('orders', []):
                if str(order.get('order_id')) == '3299' or '3299' in str(order.get('id', '')):
                    found_dashboard.append(order)
                    
    if found_dashboard:
        print(f"Found {len(found_dashboard)} items for order 3299 in Dashboard.")
        for item in found_dashboard[:3]:
            print(f" - {item.get('product_name') or item.get('cesid')} (ID: {item.get('id')})")
    else:
        print("Order 3299 NOT FOUND in Dashboard Data.")
        
    print("\\n--- Checking Raw Database for Order 3299 ---")
    
    # Check in sm_kontr_sat
    q1 = f"""
    SELECT s.idn, s.sen_no, CONVERT(VARCHAR(10), s.tarix, 23) as tarix, s.sif_sen, s.sif_form, e.mal, g.name, g.class
    FROM sm_kontr_sat s WITH (NOLOCK)
    JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    WHERE s.idn = 3299 OR s.sen_no LIKE '%3299%' OR s.sen_no = '3299'
    """
    res1 = query(q1)
    if res1:
        print("Found in sm_kontr_sat:")
        for r in res1:
            print(r)
            
    # Check in sm_sifaris_form
    q2 = f"""
    SELECT s.idn, s.sen_no, CONVERT(VARCHAR(10), s.tarix, 23) as tarix, e.mal, g.name, g.class
    FROM sm_sifaris_form s WITH (NOLOCK)
    JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    WHERE s.idn = 3299 OR s.sen_no LIKE '%3299%' OR s.sen_no = '3299'
    """
    res2 = query(q2)
    if res2:
        print("Found in sm_sifaris_form:")
        for r in res2:
            print(r)
            
    # Check in sm_sif_sened
    q3 = f"""
    SELECT s.idn, s.sen_no, CONVERT(VARCHAR(10), s.tarix, 23) as tarix, e.mal, g.name, g.class
    FROM sm_sif_sened s WITH (NOLOCK)
    JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    WHERE s.idn = 3299 OR s.sen_no LIKE '%3299%' OR s.sen_no = '3299'
    """
    res3 = query(q3)
    if res3:
        print("Found in sm_sif_sened:")
        for r in res3:
            print(r)
            
    # Check sm_sob_trans where el_sif = 3299
    q4 = f"""
    SELECT TOP 5 t.idn, t.el_sif, CONVERT(VARCHAR(10), t.tarix, 23) as tarix, t.sobe1, t.sobe2, e.mal, g.name, g.class
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el e WITH (NOLOCK) ON e.es_no = t.idn
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    WHERE t.el_sif = 3299
    """
    res4 = query(q4)
    if res4:
        print("Found in sm_sob_trans (Transfers with el_sif = 3299):")
        for r in res4:
            print(r)
        
if __name__ == "__main__":
    main()
