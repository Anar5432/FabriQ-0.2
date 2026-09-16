import os
import sys
import django

sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def main():
    with open('production_out.txt', 'w', encoding='utf-8') as f:
        f.write("=== Analyzing Wholesale vs B2B Production ===\n")
        # Total production docs
        sql_total = "SELECT COUNT(*) as cnt FROM sm_good_ist"
        total = query(sql_total)[0]['cnt']
        f.write(f"Total production docs (sm_good_ist): {total}\n")

        # Production docs with NO sif_no (order number)
        sql_null_sif = "SELECT COUNT(*) as cnt FROM sm_good_ist WHERE sif_no IS NULL OR sif_no = 0"
        null_sif = query(sql_null_sif)[0]['cnt']
        f.write(f"Production docs with NO sif_no (Wholesale?): {null_sif}\n")

        # Let's check what kind of goods are produced with NO sif_no
        sql_wholesale_goods = """
        SELECT TOP 50 g.class, g.name, e.miqdar
        FROM sm_good_ist i
        JOIN sm_good_ist_el e ON e.es_no = i.idn
        JOIN sm_goods g ON e.mal = g.idn
        WHERE i.sif_no IS NULL OR i.sif_no = 0
        ORDER BY i.tarix DESC
        """
        goods = query(sql_wholesale_goods)
        f.write("\nRecent Wholesale productions:\n")
        for g in goods:
            f.write(f"Name: {g['name']}, Class: {g['class']}, Qty: {g['miqdar']}\n")

if __name__ == "__main__":
    main()
