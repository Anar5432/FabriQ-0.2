import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    cols = query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_sifaris_form_el'")
    print([c['COLUMN_NAME'] for c in cols])
    
    # Check if there is a 'qaliq' or status column
    rows = query("SELECT TOP 5 miqdar, emeliyyat, get_miq FROM sm_sifaris_form_el ORDER BY idn DESC")
    for r in rows:
        print(r)
        
if __name__ == '__main__':
    check_logic()
