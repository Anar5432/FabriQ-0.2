import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    rows = query("SELECT TOP 5 miqdar, qaliq, sif_miq FROM sm_sifaris_form_el ORDER BY idn DESC")
    for r in rows:
        print(r)
        
    res = query("SELECT COUNT(*) as c FROM sm_sifaris_form_el WHERE qaliq > 0")
    print(f"Total rows with qaliq > 0: {res[0]['c']}")
    
    res2 = query("SELECT COUNT(*) as c FROM sm_sifaris_form_el WHERE qaliq = 0")
    print(f"Total rows with qaliq = 0: {res2[0]['c']}")

if __name__ == '__main__':
    check_logic()
