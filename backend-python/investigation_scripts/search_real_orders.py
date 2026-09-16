import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def search_database():
    print("--- Searching for specific orders in the database ---")
    
    # Let's search companies for EKIN or Adonis
    companies = query("SELECT id, name FROM sm_companies WHERE name LIKE '%EKIN%' OR name LIKE '%Adonis%'")
    print("\nCompanies Found:")
    for c in companies:
        print(f"ID: {c['id']} | Name: {c['name']}")
        
    company_ids = [c['id'] for c in companies]
    if not company_ids:
        print("No companies found with EKIN or Adonis. Let's try to find 'Adonis' in product names or comments.")
        
    # Let's search sm_sifaris_form (Pending Orders)
    print("\nSearching sm_sifaris_form (Order Form)...")
    try:
        q_sif = "SELECT idn, sen_no, tarix, kontra, mebleg, ins_user, ins_date FROM sm_sifaris_form WHERE tarix >= DATEADD(DAY, -10, GETDATE())"
        sif_records = query(q_sif)
        print(f"Total recent records in sm_sifaris_form: {len(sif_records)}")
        for r in sif_records:
            if r['mebleg'] == 27 or r['mebleg'] == 20 or r['kontra'] in company_ids or 'aytekin' in str(r.get('ins_user','')).lower() or 'yusif' in str(r.get('ins_user','')).lower():
                print(f"MATCH in sm_sifaris_form: {r}")
    except Exception as e:
        print("Error in sm_sifaris_form:", str(e))
        
    # Let's search sm_kontr_sat (Sales)
    print("\nSearching sm_kontr_sat (Confirmed Sales)...")
    try:
        q_sat = "SELECT idn, sen_no, tarix, kontra, kontra_name, tam_yek, ins_user, ins_date FROM sm_kontr_sat WHERE tarix >= DATEADD(DAY, -10, GETDATE())"
        sat_records = query(q_sat)
        print(f"Total recent records in sm_kontr_sat: {len(sat_records)}")
        for r in sat_records:
            if r['tam_yek'] == 27 or r['tam_yek'] == 20 or r['kontra'] in company_ids or 'aytekin' in str(r.get('ins_user','')).lower() or 'yusif' in str(r.get('ins_user','')).lower():
                print(f"MATCH in sm_kontr_sat: {r}")
    except Exception as e:
        print("Error in sm_kontr_sat:", str(e))
        
    # Search sm_kontr_sif_sat (Sales Orders)
    print("\nSearching sm_kontr_sif_sat (Sales Orders)...")
    try:
        q_sif_sat = "SELECT idn, sen_no, tarix, kontra, tam_yek, ins_user, ins_date FROM sm_kontr_sif_sat WHERE tarix >= DATEADD(DAY, -10, GETDATE())"
        sif_sat_records = query(q_sif_sat)
        print(f"Total recent records in sm_kontr_sif_sat: {len(sif_sat_records)}")
        for r in sif_sat_records:
            if r['tam_yek'] == 27 or r['tam_yek'] == 20 or r['kontra'] in company_ids or 'aytekin' in str(r.get('ins_user','')).lower() or 'yusif' in str(r.get('ins_user','')).lower():
                print(f"MATCH in sm_kontr_sif_sat: {r}")
    except Exception as e:
        print("Error in sm_kontr_sif_sat:", str(e))

if __name__ == '__main__':
    search_database()
