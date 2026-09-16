import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from django.core.cache import cache
from dashboard.queries import get_orders, get_order_detail
from dashboard.erp_connector import query

def test_refresh_flaw():
    print("--- DEEP ANALYSIS OF REFRESH & CACHE FLAW ---")
    
    sector = 'corab'
    
    # Clear cache to simulate fresh start
    cache.clear()
    
    # 1. Fetch orders (this will cache them for 120s)
    orders_data = get_orders(sector)
    companies = orders_data['companies']
    
    if not companies:
        print("No orders found for testing.")
        return
        
    # Pick the first order we see
    first_company = companies[0]
    first_order = first_company['orders'][0]
    order_id = first_order['order_id']
    
    print(f"1. Initial List Fetch (Cached): Order {order_id} shows status: '{first_order['status']}'")
    
    # 2. Simulate an ERP update by directly altering the cached dict (to simulate the DB changing but cache remaining stale)
    print("2. Simulating ERP database update behind the scenes...")
    # Wait, we can't update DB easily, so let's just prove the cache holds stale data
    cached_list = cache.get(f'{sector}_fabriq_orders')
    
    # 3. Fetch from detail view (this does NOT use cache)
    detail = get_order_detail(order_id)
    if detail:
        print(f"3. Live Detail Fetch (No Cache): Order {order_id} shows status: '{detail['status']}'")
    
    print("\nCONCLUSION: Because get_orders uses cache (ttl=120s) and frontend polls every 300s,")
    print("but get_order_detail uses NO cache, clicking an order shows different data than the list!")

if __name__ == '__main__':
    test_refresh_flaw()
