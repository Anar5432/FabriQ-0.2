# -*- coding: utf-8 -*-
import sys, os, django
sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders

def report():
    print("Fetching orders using the latest Virtual Ledger logic...")
    # Fetch isci orders
    data = get_orders(sector='isci')
    companies = data.get('companies', [])
    
    all_lines = []
    for c in companies:
        all_lines.extend(c.get('orders', []))
        
    target_ids = ['900162', '900163', '900165', '900168', '900169', '900166']
    
    print("\n--- TARGET ORDERS REPORT ---")
    found_targets = []
    for line in all_lines:
        # Safely find the order ID string
        order_id_str = str(line.get('order_no') or line.get('sifaris_no') or line.get('idn') or line.get('id', ''))
        
        for tid in target_ids:
            if tid in order_id_str:
                found_targets.append(line)
                print(f"--- MATCH: {order_id_str} ---")
                print(f"Full data: {line}")
                print("-" * 40)
                
    if not found_targets:
        print("Could not find the target orders in the active list. They might be completed or have a different ID format.")
        
    print("\n--- 3 ACTIVE ORDERS IN DIFFERENT STAGES FOR TESTING ---")
    
    found_stages = set()
    examples = []
    
    for line in all_lines:
        stage_id = line.get('stage_id', '0')
        
        # Look for active phases (not 0 and not 4/5 which are completed depending on sector)
        if stage_id not in ('0', '4', '5'):
            if stage_id not in found_stages:
                found_stages.add(stage_id)
                examples.append(line)
            
            if len(examples) == 3:
                break
                
    for ex in examples:
        print(f"Customer: {ex.get('sector_name', 'Unknown')}")
        print(f"Order: {ex.get('id')} | Product: {ex.get('cesid', 'Unknown')}")
        print(f"Qty: {ex.get('miqdar')}")
        print(f"Stage: {ex.get('phase_name', 'Unknown')} (ID: {ex.get('stage_id')})")
        print("-" * 40)

if __name__ == '__main__':
    report()
