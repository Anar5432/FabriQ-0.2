import os
import sys
import django

sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def main():
    print("=== Finding Underwear Classes ===")
    sql_classes = "SELECT DISTINCT class, name FROM sm_goods WHERE name LIKE '%alt%' OR name LIKE '%penn%' OR name LIKE '%peny%' OR name LIKE '%under%'"
    classes = query(sql_classes)
    for c in classes:
        print(c)
        
    print("\n=== Finding Class names ===")
    sql_all_classes = "SELECT idn, name FROM sm_class"
    all_c = query(sql_all_classes)
    for c in all_c:
        if 'alt' in str(c['name']).lower() or 'pen' in str(c['name']).lower() or 'iç' in str(c['name']).lower() or 'ic ' in str(c['name']).lower() or 'tuman' in str(c['name']).lower():
            print(c)

if __name__ == "__main__":
    main()
