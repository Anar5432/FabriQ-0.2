import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    print("Columns for sm_sifaris_qaime_el:")
    q = "SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_sifaris_qaime_el'"
    rows = query(q)
    for r in rows: print(r)

if __name__ == '__main__':
    check_logic()
