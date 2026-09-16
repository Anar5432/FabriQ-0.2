import os
import sys
sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.planning_engine import PlanningEngine

e = PlanningEngine()
e.load_workers()
e.load_inventory_and_backlog()

print("\n--- Searching for product with operations ---")
found_product = None
for p in e.active_orders:
    ops = e.fetch_categorized_operations(p.product_id)
    if any(len(v)>0 for v in ops.values()):
        found_product = p
        break

if not found_product:
    print("NO PRODUCTS WITH OPERATIONS IN THE ENTIRE BACKLOG???")
    sys.exit(0)

p = found_product
print(f"Product: {p.product_id} - {p.product_name} (Qty: {p.qty})")

print("\nOperations by Phase:")
ops = e.fetch_categorized_operations(p.product_id)
print(ops)

print("\nRunning simulate_product directly:")
r = e.simulate_product(p.product_id, p.qty, sourcing_days=0, is_backlog=False)
print("Assignments:")
for a in r.get('assignments', []):
    print(f"[{a['start']} -> {a['end']}] {a['phase']} - {a['op_name']} : {a['name']} ({a['qty']} pcs)")
