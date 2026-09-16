import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query
from dashboard.queries import get_orders

with open('investigate_debt_bug_2.txt', 'w', encoding='utf-8') as f:
    try:
        sql_cust_balance = "SELECT TOP 1 kontra FROM sm_borc"
        res_borc = query(sql_cust_balance)
        f.write(f"Type in sm_borc: {type(res_borc[0]['kontra'])}\n")
        
        sql_sat = "SELECT TOP 1 kontra FROM sm_kontr_sat"
        res_sat = query(sql_sat)
        f.write(f"Type in sm_kontr_sat: {type(res_sat[0]['kontra'])}\n")

    except Exception as e:
        f.write(f"Error: {e}\n")
