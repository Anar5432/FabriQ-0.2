import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def inspect():
    # Let's see what columns are in sm_sifaris_form
    cols = query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_sifaris_form'")
    print("Columns in sm_sifaris_form:", [c['COLUMN_NAME'] for c in cols])
    
    # Check the latest order in sm_sifaris_form
    res = query("SELECT TOP 1 * FROM sm_sifaris_form ORDER BY idn DESC")
    print("\nLatest order in sm_sifaris_form:", res[0])

if __name__ == '__main__':
    inspect()
