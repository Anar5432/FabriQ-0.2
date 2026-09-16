import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    print("--- Checking 'tes' (tesdiq/approved) in sm_sifaris_form ---")
    res1 = query("SELECT tes, COUNT(*) as c FROM sm_sifaris_form GROUP BY tes")
    for r in res1:
        print(f"Tesdiq Status {r['tes']}: {r['c']} orders")
        
    print("\n--- Checking links from sm_kontr_sat to sm_sifaris_form ---")
    res2 = query("SELECT COUNT(*) as c FROM sm_kontr_sat WHERE sif_idn IS NOT NULL OR sif_form IS NOT NULL")
    print(f"Orders in sm_kontr_sat linked to a Sifaris Form: {res2[0]['c']}")

    print("\n--- Let's look at the 'Adonis' or 'EKIN' orders ---")
    res3 = query("SELECT idn, sen_no, tes FROM sm_sifaris_form WHERE idn IN (22384, 21673, 21801)")
    for r in res3:
        print(f"Specific Order {r['idn']} -> Tesdiq: {r['tes']}")

if __name__ == '__main__':
    check_logic()
