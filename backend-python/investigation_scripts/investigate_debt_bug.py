import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query
from dashboard.queries import get_orders

with open('investigate_debt_bug.txt', 'w', encoding='utf-8') as f:
    try:
        # 1. Check actual debts in sm_borc
        sql_borc = """
        SELECT TOP 10 kontra, kon_name, SUM(yekun) as total_debt
        FROM sm_borc
        GROUP BY kontra, kon_name
        HAVING SUM(yekun) > 100
        ORDER BY total_debt DESC
        """
        f.write("=== Top 10 Debtors in sm_borc ===\n")
        borc_rows = query(sql_borc)
        for r in borc_rows:
            f.write(f"Kontra: {r['kontra']} | Name: {r['kon_name']} | Debt: {r['total_debt']}\n")

        # 2. Let's see what get_orders() returns
        f.write("\n=== Testing get_orders() output ===\n")
        # Just grab the active companies
        res = get_orders(sector='isci', status_filter='all')
        companies = res['companies']
        
        f.write(f"Fetched {len(companies)} companies in 'isci' sector.\n")
        # Let's print the first 5 companies
        for i, c in enumerate(companies[:5]):
            f.write(f"Company ID: {c['id']} | Name: {c['name']} | Total Debt: {c['total_debt']} | Total Ordered: {c['total_ordered']} | Total Paid: {c['total_paid']}\n")
            
        # Is the 'id' in companies a string or int? 
        # Is 'kontra' in sm_borc a string or int?
        
        f.write("\n=== Checking types ===\n")
        if borc_rows:
            f.write(f"sm_borc kontra type: {type(borc_rows[0]['kontra'])}\n")
        if companies:
            f.write(f"companies id type: {type(companies[0]['id'])}\n")

    except Exception as e:
        f.write(f"Error: {e}\n")
