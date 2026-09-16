import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_tables():
    print("Latest 5 sm_kontr_sat:")
    res = query("SELECT TOP 5 sen_no, tarix, ins_date FROM sm_kontr_sat ORDER BY idn DESC")
    for r in res:
        print(r)
        
    print("\nLatest 5 sm_sifaris_form:")
    try:
        res = query("SELECT TOP 5 idn, tarix, ins_date FROM sm_sifaris_form ORDER BY idn DESC")
        for r in res:
            print(r)
    except:
        pass
        
    print("\nLatest 5 sm_sif_sec:")
    try:
        res = query("SELECT TOP 5 idn, tarix, ins_date FROM sm_sif_sec ORDER BY idn DESC")
        for r in res:
            print(r)
    except:
        pass

if __name__ == '__main__':
    check_tables()
