import os
import sys
import django

sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def main():
    with open('underwear_out.txt', 'w', encoding='utf-8') as f:
        f.write("=== Finding Class names ===\n")
        sql_all_classes = "SELECT idn, name FROM sm_good_class"
        all_c = query(sql_all_classes)
        for c in all_c:
            name_lower = str(c['name']).lower()
            if 'alt' in name_lower or 'peny' in name_lower or 'iç ' in name_lower or 'ic ' in name_lower or 'tuman' in name_lower:
                f.write(f"Class: {c['idn']} - {c['name']}\n")
                
        f.write("\n=== Underwear Goods ===\n")
        # Find some examples of goods
        sql_goods = "SELECT TOP 50 idn, name, class FROM sm_goods WHERE name LIKE '%peny%' OR name LIKE '%alt paltar%'"
        goods = query(sql_goods)
        for g in goods:
            f.write(f"Good: {g['idn']} - {g['name']} (Class: {g['class']})\n")

if __name__ == "__main__":
    main()
