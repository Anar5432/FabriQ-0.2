import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_tables():
    tables_to_check = ['sm_kontr_sif_sat', 'sm_kontr_sif_sat_el', 'mob_sifaris', 'sm_telebname']
    
    for t in tables_to_check:
        try:
            res = query(f"SELECT COUNT(*) as c FROM {t} WHERE tarix >= DATEADD(DAY, -2, GETDATE())")
            print(f"{t} recent records: {res[0]['c']}")
        except Exception as e:
            print(f"Error checking {t}: {str(e)}")
            
    # Check what the most recent record in sm_kontr_sat is
    try:
        res = query("SELECT TOP 1 tarix FROM sm_kontr_sat ORDER BY tarix DESC")
        if res:
            print(f"Most recent sm_kontr_sat: {res[0]['tarix']}")
    except:
        pass

if __name__ == '__main__':
    check_tables()
