import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_today():
    print("Checking today's orders...")
    
    # 1. Check sm_kontr_sat (Sales to Customer - current query source)
    q_sat = "SELECT COUNT(*) as c FROM sm_kontr_sat WHERE tarix >= CONVERT(date, GETDATE())"
    res_sat = query(q_sat)
    print(f"Today's records in sm_kontr_sat (Sales): {res_sat[0]['c']}")
    
    # 2. Check sm_sifaris_form (Internal Order / Requisition?)
    q_sif = "SELECT COUNT(*) as c FROM sm_sifaris_form WHERE tarix >= CONVERT(date, GETDATE())"
    try:
        res_sif = query(q_sif)
        print(f"Today's records in sm_sifaris_form: {res_sif[0]['c']}")
    except Exception as e:
        print("sm_sifaris_form error:", str(e))
        
    # 3. Check sm_sifaris (Main Orders header?)
    q_sif_hdr = "SELECT COUNT(*) as c FROM sm_sifaris WHERE tarix >= CONVERT(date, GETDATE())"
    try:
        res_sif_hdr = query(q_sif_hdr)
        print(f"Today's records in sm_sifaris: {res_sif_hdr[0]['c']}")
    except Exception as e:
        print("sm_sifaris error:", str(e))

if __name__ == '__main__':
    check_today()
