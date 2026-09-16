import os, django, sys
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()
from dashboard.erp_connector import query

def check():
    sql = """
    SELECT TABLE_NAME, TABLE_TYPE 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_NAME LIKE '%qaliq%' 
       OR TABLE_NAME LIKE '%stok%'
       OR TABLE_NAME LIKE '%hereket%'
       OR TABLE_NAME LIKE '%rezerv%'
       OR TABLE_NAME LIKE '%sened%'
    """
    res = query(sql)
    for r in res:
        print(f"{r['TABLE_NAME']} ({r['TABLE_TYPE']})")

if __name__ == '__main__':
    check()
