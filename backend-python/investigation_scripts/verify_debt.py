import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders

with open('investigate_debt_bug_3.txt', 'w', encoding='utf-8') as f:
    try:
        # Fetch orders for all sectors to check debts
        res = get_orders(sector='isci')
        companies = res['companies']
        
        f.write(f"Fetched {len(companies)} companies.\n")
        f.write("=== Companies with debt > 0 ===\n")
        
        count = 0
        for c in companies:
            if c['total_debt'] != 0:
                count += 1
                f.write(f"Company ID: {c['id']} | Name: {c['name']} | Total Debt: {c['total_debt']} | Total Ordered: {c['total_ordered']} | Total Paid: {c['total_paid']}\n")
        
        f.write(f"\nTotal companies with non-zero debt: {count}\n")
        
        if count == 0:
            f.write("ERROR: Still 0 companies with debt! Let's check a specific one, e.g., BİNƏ T/M\n")

    except Exception as e:
        f.write(f"Error: {e}\n")
