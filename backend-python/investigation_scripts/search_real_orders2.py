import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def search_database():
    print("--- Deep Searching For EKIN and Adonis ---")
    
    # 1. Search in sm_sifaris_form (Pending Orders)
    print("\n--- sm_sifaris_form ---")
    try:
        q_sif = "SELECT idn, sen_no, tarix, kontra, mebleg, ins_user FROM sm_sifaris_form WHERE tarix >= DATEADD(DAY, -15, GETDATE())"
        sif_records = query(q_sif)
        print(f"Total recent records: {len(sif_records)}")
        for r in sif_records:
            if 'ekin' in str(r.get('ins_user','')).lower() or 'adonis' in str(r.get('ins_user','')).lower() or r['mebleg'] == 27 or r['mebleg'] == 20 or 'aytekin' in str(r.get('ins_user','')).lower() or 'yusif' in str(r.get('ins_user','')).lower():
                print(f"MATCH: {r}")
    except Exception as e:
        print("Error:", str(e))
        
    # 2. Search in sm_sifaris (Sales Orders Header?)
    print("\n--- sm_sifaris ---")
    try:
        q_sif_h = "SELECT idn, sen_no, tarix, kontra, mebleg, ins_user FROM sm_sifaris WHERE tarix >= DATEADD(DAY, -15, GETDATE())"
        sif_h_records = query(q_sif_h)
        print(f"Total recent records: {len(sif_h_records)}")
        for r in sif_h_records:
            if r['mebleg'] == 27 or r['mebleg'] == 20 or 'aytekin' in str(r.get('ins_user','')).lower() or 'yusif' in str(r.get('ins_user','')).lower():
                print(f"MATCH: {r}")
    except Exception as e:
        print("Error:", str(e))

    # 3. Search in sm_kontr_sat (Sales Invoices)
    print("\n--- sm_kontr_sat ---")
    try:
        q_sat = "SELECT idn, sen_no, tarix, kontra_name, tam_yek, ins_user FROM sm_kontr_sat WHERE tarix >= DATEADD(DAY, -15, GETDATE())"
        sat_records = query(q_sat)
        print(f"Total recent records: {len(sat_records)}")
        for r in sat_records:
            kontra = str(r.get('kontra_name','')).lower()
            ins = str(r.get('ins_user','')).lower()
            if 'ekin' in kontra or 'adonis' in kontra or r['tam_yek'] == 27 or r['tam_yek'] == 20 or 'aytekin' in ins or 'yusif' in ins:
                print(f"MATCH: {r}")
    except Exception as e:
        print("Error:", str(e))
        
    # 4. Search in sm_goods (Products)
    print("\n--- sm_goods ---")
    try:
        q_goods = "SELECT idn, name, class FROM sm_goods WHERE name LIKE '%EKIN%' OR name LIKE '%Adonis%'"
        goods_records = query(q_goods)
        for r in goods_records:
            print(f"MATCH PRODUCT: {r}")
    except Exception as e:
        print("Error:", str(e))

if __name__ == '__main__':
    search_database()
