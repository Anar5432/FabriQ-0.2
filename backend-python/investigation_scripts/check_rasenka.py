import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_rasenka():
    print("sm_rasenka_mal columns:")
    cols = query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_rasenka_mal'")
    print([c['COLUMN_NAME'] for c in cols])
    
    print("sm_rasenka_el columns:")
    cols = query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_rasenka_el'")
    print([c['COLUMN_NAME'] for c in cols])
    
    # We want to find orders without rasenka. Let's see what tables represent orders.
    # We know sm_sifaris is the order table. Let's check.
    # Or sm_smeta?
    cols = query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_sifaris'")
    print("sm_sifaris columns:")
    print([c['COLUMN_NAME'] for c in cols])

if __name__ == '__main__':
    check_rasenka()
