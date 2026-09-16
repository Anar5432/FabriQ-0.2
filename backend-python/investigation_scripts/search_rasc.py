import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def find_rasc():
    tables = query("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    for t in tables:
        t_name = t['TABLE_NAME'].lower()
        if 'rasc' in t_name or 'rasc' in t_name:
            print(f"Found table: {t_name}")
            
    columns = query("SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME LIKE '%rasc%' OR COLUMN_NAME LIKE '%qiymet%' OR COLUMN_NAME LIKE '%mebleg%'")
    for c in columns:
        print(f"Found column: {c['TABLE_NAME']}.{c['COLUMN_NAME']}")

if __name__ == '__main__':
    find_rasc()
