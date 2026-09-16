import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_rasenka():
    tables = query("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE 'sm_rasenka%'")
    for t in tables:
        t_name = t['TABLE_NAME']
        print(f"Table: {t_name}")
        cols = query(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{t_name}'")
        print([c['COLUMN_NAME'] for c in cols])

if __name__ == '__main__':
    check_rasenka()
