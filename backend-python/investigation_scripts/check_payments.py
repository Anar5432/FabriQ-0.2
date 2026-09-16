import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

with open('investigate_payments.txt', 'w', encoding='utf-8') as f:
    sql = """
    SELECT TOP 1 kontra, yekun FROM sm_kmd
    """
    try:
        f.write(f"sm_kmd: {query(sql)}\n")
    except Exception as e:
        f.write(f"Error kmd: {e}\n")
        
    sql2 = """
    SELECT TOP 1 kontra, yekun FROM sm_bank_od
    """
    try:
        f.write(f"sm_bank_od: {query(sql2)}\n")
    except Exception as e:
        f.write(f"Error bank: {e}\n")
