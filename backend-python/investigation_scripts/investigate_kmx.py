import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

with open('investigate_results3.txt', 'w', encoding='utf-8') as f:
    try:
        sql = """
        SELECT TOP 10 k.tarix, k.mebleg, k.serh, k.kontra, xm.new_madde, xm.qrup
        FROM sm_kassa_transfer k
        """
        # Wait, xerc_maddeleri usually maps to sm_xerc or sm_kmx_el. Let's look at sm_kmx_el columns.
        sql_cols = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_kmx_el'"
        f.write(f"sm_kmx_el columns: {[c['COLUMN_NAME'] for c in query(sql_cols)]}\n")
        
        # Look for xerc column in sm_kmx
        sql_cols2 = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_kmx'"
        f.write(f"sm_kmx columns: {[c['COLUMN_NAME'] for c in query(sql_cols2)]}\n")
        
    except Exception as e:
        f.write(f"Error: {e}\n")

