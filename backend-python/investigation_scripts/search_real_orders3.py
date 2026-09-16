import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def search_database():
    out = io.StringIO()
    out.write("--- Deep Searching For EKIN and Adonis ---\n")
    
    # 1. Search in sm_sifaris_form (Pending Orders)
    try:
        q_sif = "SELECT idn, sen_no, tarix, kontra, mebleg, ins_user FROM sm_sifaris_form WHERE tarix >= DATEADD(DAY, -15, GETDATE())"
        sif_records = query(q_sif)
        out.write(f"\n--- sm_sifaris_form ({len(sif_records)} recent records) ---\n")
        for r in sif_records:
            user = str(r.get('ins_user','')).lower()
            if 'ekin' in user or 'adonis' in user or r['mebleg'] == 27 or r['mebleg'] == 20 or 'ayt' in user or 'yusif' in user:
                out.write(f"MATCH: {r}\n")
    except Exception as e:
        out.write(f"Error: {e}\n")
        
    # 3. Search in sm_kontr_sat (Sales Invoices)
    try:
        q_sat = "SELECT idn, sen_no, tarix, kontra_name, tam_yek, ins_user FROM sm_kontr_sat WHERE tarix >= DATEADD(DAY, -15, GETDATE())"
        sat_records = query(q_sat)
        out.write(f"\n--- sm_kontr_sat ({len(sat_records)} recent records) ---\n")
        for r in sat_records:
            kontra = str(r.get('kontra_name','')).lower()
            ins = str(r.get('ins_user','')).lower()
            if 'ekin' in kontra or 'adonis' in kontra or r['tam_yek'] == 27 or r['tam_yek'] == 20 or 'ayt' in ins or 'yusif' in ins:
                out.write(f"MATCH: {r}\n")
    except Exception as e:
        out.write(f"Error: {e}\n")
        
    # Search sm_kontr_sif_sat (Sales Orders? Or is it mob_sifaris?)
    try:
        q_mob = "SELECT * FROM sm_kontr_sif_sat WHERE tarix >= DATEADD(DAY, -15, GETDATE())"
        mob_records = query(q_mob)
        out.write(f"\n--- sm_kontr_sif_sat ({len(mob_records)} recent records) ---\n")
    except Exception as e:
        pass
        
    # 4. Search in sm_goods (Products)
    try:
        q_goods = "SELECT idn, name, class FROM sm_goods WHERE name LIKE '%EKIN%' OR name LIKE '%Adonis%'"
        goods_records = query(q_goods)
        out.write("\n--- sm_goods ---\n")
        for r in goods_records:
            out.write(f"MATCH PRODUCT: {r}\n")
    except Exception as e:
        out.write(f"Error: {e}\n")

    with io.open("search_results.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    search_database()
